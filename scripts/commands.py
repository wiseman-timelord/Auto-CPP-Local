import json, datetime
from config import Config
from memory import LocalCache
import agent_manager as agents
from ai_functions import *
from operations import *
from json_parser import fix_and_parse_json
from duckduckgo_search import ddg
from googleapiclient.discovery import build, HttpError

cfg = Config()

def is_valid_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def get_command(response):
    try:
        res_json = fix_and_parse_json(response)
        cmd = res_json.get("command", {})
        return cmd.get("name", "Error: Missing 'name'"), cmd.get("args", {})
    except (json.JSONDecodeError, Exception) as e:
        return "Error:", str(e)

def execute_command(command_name, arguments):
    memory = LocalCache(cfg)
    try:
        if command_name == "google":
            return google_official_search(arguments["input"]) if cfg.google_api_key.strip() else google_search(arguments["input"])
        if command_name == "memory_add":
            return memory.add(arguments["string"])
        if command_name == "start_agent":
            return start_agent(arguments["name"], arguments["task"], arguments["prompt"])
        if command_name == "message_agent":
            return message_agent(arguments["key"], arguments["message"])
        if command_name == "list_agents":
            return list_agents()
        if command_name == "delete_agent":
            return delete_agent(arguments["key"])
        if command_name == "get_text_summary":
            return get_text_summary(arguments["url"], arguments["question"])
        if command_name == "get_hyperlinks":
            return get_hyperlinks(arguments["url"])
        if command_name == "read_file":
            return read_file(arguments["file"])
        if command_name == "write_to_file":
            return write_to_file(arguments["file"], arguments["text"])
        if command_name == "append_to_file":
            return append_to_file(arguments["file"], arguments["text"])
        if command_name == "delete_file":
            return delete_file(arguments["file"])
        if command_name == "search_files":
            return search_files(arguments["directory"])
        if command_name == "browse_website":
            return browse_website(arguments["url"], arguments["question"])
        if command_name == "evaluate_code":
            return model.create_completion(arguments["code"], max_tokens=1500)
        if command_name == "improve_code":
            return model.create_completion(f"Improve the code:\n\n{arguments['code']}\n\nSuggestions:\n{arguments['suggestions']}", max_tokens=1500)
        if command_name == "write_tests":
            return model.create_completion(f"Write tests:\n\n{arguments['code']}\n\nFocus: {arguments.get('focus', 'all aspects')}", max_tokens=1500)
        if command_name == "execute_python_file":
            return execute_python_file(arguments["file"])
        if command_name == "execute_shell":
            return execute_shell(arguments["command_line"]) if cfg.execute_local_commands else "Not allowed to run local shell commands."
        if command_name == "generate_image":
            return generate_image(arguments["prompt"])
        if command_name == "do_nothing":
            return "No action performed."
        if command_name == "task_complete":
            shutdown()
        return f"Unknown command '{command_name}'."
    except Exception as e:
        return "Error: " + str(e)

def get_datetime():
    return "Current date/time: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def browse_website(url, question):
    summary = get_text_summary(url, question)
    links = get_hyperlinks(url)[:5]
    return f"Website Summary: {summary}\nLinks: {links}"

def get_text_summary(url, question):
    text = scrape_text(url)
    return "Result: " + summarize_text(url, text, question)

def get_hyperlinks(url):
    return scrape_links(url)

def commit_memory(string):
    mem.permanent_memory.append(string)
    return f"Memory committed: {string}"

def delete_memory(key):
    if 0 <= key < len(mem.permanent_memory):
        del mem.permanent_memory[key]
        return f"Memory {key} deleted."
    return "Invalid key."

def overwrite_memory(key, string):
    if is_valid_int(key) and 0 <= int(key) < len(mem.permanent_memory):
        mem.permanent_memory[int(key)] = string
        return f"Memory {key} overwritten with: {string}"
    elif isinstance(key, str):
        mem.permanent_memory[key] = string
        return f"Memory {key} overwritten with: {string}"
    return "Invalid key."

def shutdown():
    print("Shutting down...")
    quit()

def start_agent(name, task, prompt, model=cfg.fast_llm_model):
    key, ack = agents.create_agent(task, f"You are {name}. Acknowledged.", model)
    return f"Agent {name} created with key {key}. First response: {message_agent(key, prompt)}"

def message_agent(key, message):
    response = agents.message_agent(int(key) if is_valid_int(key) else key, message)
    return response

def list_agents():
    return agents.list_agents()

def delete_agent(key):
    return f"Agent {key} deleted." if agents.delete_agent(key) else f"Agent {key} does not exist."
