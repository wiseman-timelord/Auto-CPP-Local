# `.\scripts\management.py`

# Imports
from models import create_chat_completion, call_ai_function
from typing import List, Optional, Tuple
import json, requests, os
from config import Config
from models import call_ai_function, create_chat_completion
from utilities import LocalCache, logger, TaskTracker
from urllib.parse import urlparse, urljoin
import argparse, logging
from operations import ingest_file, search_files, evaluate_task_success, break_down_task

# Globals
next_key = 0
agents = {}  # key: (task, history, model)
cfg = Config()
memory = LocalCache(cfg)
model = Llama(model_path=cfg.llm_model_settings['smart_llm_model'])
task_tracker = TaskTracker()  # Initialize TaskTracker for managing tasks
WORKSPACE_FOLDER = ".\workspace"
session = requests.Session()
session.headers.update({'User-Agent': cfg.browsing_settings['user_agent']})

def configure_logging():
    logging.basicConfig(filename='log-ingestion.txt',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)
    return logging.getLogger('AutoGPT-Ingestion')

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def sanitize_url(url):
    return urljoin(url, urlparse(url).path)

def check_local_file_access(url):
    return any(url.startswith(prefix) for prefix in ['file:///', 'file://localhost', 'http://localhost', 'https://localhost'])

def get_response(url, timeout=10):
    try:
        if check_local_file_access(url):
            raise ValueError('Restricted local file access')
        if not url.startswith(('http://', 'https://')):
            raise ValueError('Invalid URL')
        response = session.get(sanitize_url(url), timeout=timeout)
        return (response, None) if response.status_code < 400 else (None, f"HTTP {response.status_code}")
    except (ValueError, requests.exceptions.RequestException) as e:
        return None, str(e)

def scrape_text(url):
    response, error = get_response(url)
    if error: return error
    soup = BeautifulSoup(response.text, "html.parser")
    return '\n'.join(chunk.strip() for line in soup.stripped_strings for chunk in line.split("  "))

def extract_hyperlinks(soup):
    return [(link.text, link['href']) for link in soup.find_all('a', href=True)]

def format_hyperlinks(hyperlinks):
    return [f"{text} ({url})" for text, url in hyperlinks]

def scrape_links(url):
    response, error = get_response(url)
    if error: return error
    soup = BeautifulSoup(response.text, "html.parser")
    return format_hyperlinks(extract_hyperlinks(soup))

def split_text(text, max_length=cfg.browse_chunk_max_length):
    paragraphs, current_chunk = text.split("\n"), []
    current_length = 0
    for paragraph in paragraphs:
        if current_length + len(paragraph) + 1 <= max_length:
            current_chunk.append(paragraph)
            current_length += len(paragraph) + 1
        else:
            yield "\n".join(current_chunk)
            current_chunk, current_length = [paragraph], len(paragraph) + 1
    if current_chunk:
        yield "\n".join(current_chunk)

def create_message(chunk, question):
    return {"role": "user", "content": f"\"\"\"{chunk}\"\"\" Answer: \"{question}\"."}

def summarize_text(url, text, question):
    if not text: return "No text to summarize"
    summaries, chunks = [], list(split_text(text))
    for i, chunk in enumerate(chunks):
        memory.add(f"Source: {url}\nRaw part#{i + 1}: {chunk}")
        summary = model.create_completion(
            create_message(chunk, question), 
            max_tokens=cfg.browse_summary_max_token, 
            temperature=cfg.temperature)['choices'][0]['text']
        summaries.append(summary)
        memory.add(f"Source: {url}\nSummary part#{i + 1}: {summary}")
    return model.create_completion(
        "\n".join(summaries), 
        max_tokens=cfg.browse_summary_max_token, 
        temperature=cfg.temperature)['choices'][0]['text']

def evaluate_code(code: str) -> List[str]:
    return call_ai_function(
        "def analyze_code(code: str) -> List[str]:", 
        [code], 
        "Analyzes the code and suggests improvements."
    )

def improve_code(suggestions: List[str], code: str) -> str:
    return call_ai_function(
        "def generate_improved_code(suggestions: List[str], code: str) -> str:", 
        [json.dumps(suggestions), code], 
        "Improves code based on suggestions."
    )

def write_tests(code: str, focus: List[str]) -> str:
    return call_ai_function(
        "def create_test_cases(code: str, focus: Optional[str] = None) -> str:", 
        [code, json.dumps(focus)], 
        "Generates test cases."
    )

def ingest_directory(directory, memory, args):
    try:
        for file in search_files(directory):
            ingest_file(file, memory, args.max_length, args.overlap)
    except Exception as e:
        print(f"Ingestion error in '{directory}': {e}")

def create_agent(task: str, prompt: str, model) -> Tuple[int, str]:
    global next_key, agents
    logger.debug(f"Creating agent for task: {task}")
    
    # Track the task using TaskTracker
    task_id = task_tracker.add_task(task)

    msgs = [{"role": "user", "content": prompt}]
    reply = create_chat_completion(model=model, messages=msgs)
    msgs.append({"role": "assistant", "content": reply})
    
    key = next_key
    next_key += 1
    agents[key] = (task_id, msgs, model)
    
    # Update task status to 'In Progress'
    task_tracker.update_task_status(task_id, "In Progress")
    
    return key, reply

def message_agent(key: int, message: str) -> str:
    task_id, msgs, model = agents[int(key)]
    msgs.append({"role": "user", "content": message})
    reply = create_chat_completion(model=model, messages=msgs)
    msgs.append({"role": "assistant", "content": reply})
    
    logger.debug(f"Message sent to agent {key} for task {task_id}: {message}")
    
    # Check if the task is completed based on the response
    task_result = evaluate_task_success(task_id, reply)
    if task_result['status'] == "Completed":
        task_tracker.update_task_status(task_id, "Completed")
    
    return reply

def list_agents():
    return [(k, t) for k, (t, _, _) in agents.items()]

def delete_agent(key):
    return agents.pop(int(key), None) is not None

def main():
    logger = configure_logging()
    parser = argparse.ArgumentParser(description="Ingest files into memory.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="File to ingest.")
    group.add_argument("--dir", type=str, help="Directory to ingest.")
    parser.add_argument("--init", action='store_true', help="Init and clear memory.", default=False)
    parser.add_argument("--overlap", type=int, help="Chunk overlap (default: 200)", default=200)
    parser.add_argument("--max_length", type=int, help="Chunk max length (default: 4000)", default=4000)
    args = parser.parse_args()

    memory = LocalCache(cfg)
    if args.init:
        memory.clear()
        logger.debug("Memory initialized and cleared.")
    
    if args.file:
        try:
            ingest_file(args.file, memory, args.max_length, args.overlap)
            logger.debug(f"File '{args.file}' ingested.")
        except Exception as e:
            logger.error(f"Ingest error: '{args.file}': {e}")
    elif args.dir:
        try:
            ingest_directory(args.dir, memory, args)
            logger.debug(f"Directory '{args.dir}' ingested.")
        except Exception as e:
            logger.error(f"Ingest error: '{args.dir}': {e}")
    else:
        logger.error("Provide a file (--file) or directory (--dir) to ingest.")

if __name__ == "__main__":
    main()