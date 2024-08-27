# `.\scripts\models.py`

# Imports
import subprocess, os, math, re, json
from typing import List, Dict, Any, Union
from config import Config
import tiktoken

cfg = Config()

# Classes
class LlamaModel:
    def __init__(self):
        self.model_path = None
        self.n_threads = None
        self.initialize_model()

    def initialize_model(self):
        model_dir = cfg.model_path
        self.model_path = next(
            (os.path.join(model_dir, f) for f in os.listdir(model_dir) if f.endswith(".gguf")), None)
        if not self.model_path:
            raise FileNotFoundError(f"No .gguf in {model_dir}")
        self.n_threads = self.calculate_optimal_threads()
        total_threads = os.cpu_count() or 4
        print(f"\nModel: {self.model_path}")
        print(f"Threads: {self.n_threads} ({(self.n_threads / total_threads) * 100:.2f}% CPU)")

    @staticmethod
    def calculate_optimal_threads():
        total_threads = os.cpu_count() or 4
        return math.ceil((total_threads / 100) * 85)

    def run_llama_cli(self, prompt: str, max_tokens: int, temperature: float) -> str:
        cmd = [
            ".\\data\\libraries\\LlamaCpp_Binaries\\llama-cli.exe",
            "-m", self.model_path, "-p", prompt, "--temp", str(temperature),
            "-n", str(max_tokens), "-t", str(self.n_threads), "--ctx_size", str(cfg.context_size), "-ngl", "1"
        ]
        return subprocess.run(cmd, capture_output=True, text=True).stdout

    def create_chat_completion(self, messages: List[Dict[str, str]], temperature: float = cfg.temperature, max_tokens: int = None) -> str:
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return self.run_llama_cli(prompt, max_tokens or cfg.max_tokens, temperature)

class JsonHandler:
    @staticmethod
    def fix_and_parse_json(json_str: str) -> Union[str, Dict[Any, Any]]:
        try:
            return json.loads(json_str.replace('\t', ''))
        except json.JSONDecodeError:
            return json.loads(JsonHandler.correct_json(json_str))

    @staticmethod
    def correct_json(json_str: str) -> str:
        json_str = re.sub(r'(\w+)(?=:)', r'"\1"', json_str)
        open_braces, close_braces = json_str.count('{'), json_str.count('}')
        json_str += '}' * (open_braces - close_braces)
        json_str = re.sub(r'\\([^"\/bfnrtu])', r'\1', json_str)
        return json_str

    @staticmethod
    def get_command(response: str) -> tuple:
        try:
            response_json = JsonHandler.fix_and_parse_json(response)
            if "command" not in response_json:
                return "Error:", "Missing 'command' object"
            command = response_json["command"]
            return command.get("name", "Error"), command.get("args", {})
        except json.JSONDecodeError:
            return "Error:", "Invalid JSON"
        except Exception as e:
            return "Error:", str(e)

# Functions
def count_message_tokens(messages: List[Dict[str, str]], model: str = "gpt-3.5-turbo-0301") -> int:
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    tokens_per_message, tokens_per_name = (4, -1) if model == "gpt-3.5-turbo-0301" else (3, 1)
    num_tokens = 3 + sum(tokens_per_message + sum(len(encoding.encode(value)) + (tokens_per_name if key == "name" else 0) for key, value in msg.items()) for msg in messages)
    return num_tokens

def count_string_tokens(string: str, model_name: str) -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(string))

def call_ai_function(function, args, description, model=None):
    model = model or cfg.smart_llm_model
    args = ", ".join([str(arg) if arg is not None else "None" for arg in args])
    messages = [
        {"role": "system", "content": f"You are: ```# {description}\n{function}```"},
        {"role": "user", "content": args},
    ]
    return LlamaModel().create_chat_completion(messages, temperature=0)

if __name__ == "__main__":
    llm = LlamaModel()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    print("LlamaModel response:", llm.create_chat_completion(messages))

    json_str = '{"command": {"name": "test", "args": {"key": "value"}}}'
    print("Parsed JSON:", JsonHandler.fix_and_parse_json(json_str))
    command_name, arguments = JsonHandler.get_command(json_str)
    print("Command:", command_name, "Args:", arguments)
