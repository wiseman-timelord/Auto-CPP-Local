import subprocess
import os
import math
import re
import json
from typing import List, Dict, Any, Union
from config import Config

cfg = Config()

class LlamaModel:
    def __init__(self):
        self.model_path = None
        self.n_threads = None
        self.initialize_model()

    def initialize_model(self):
        model_dir = cfg.model_path
        for file in os.listdir(model_dir):
            if file.endswith(".gguf"):
                self.model_path = os.path.join(model_dir, file)
                break
        
        if self.model_path is None:
            raise FileNotFoundError(f"No .gguf model found in {model_dir}")

        self.n_threads = self.calculate_optimal_threads()
        total_threads = os.cpu_count() or 4
        thread_usage_percentage = (self.n_threads / total_threads) * 100
        print(f"\nModel initialized: {self.model_path}")
        print(f"Using {self.n_threads} threads ({thread_usage_percentage:.2f}% of available CPU threads).")

    @staticmethod
    def calculate_optimal_threads():
        total_threads = os.cpu_count() or 4
        return math.ceil((total_threads / 100) * 85)

    def run_llama_cli(self, prompt: str, max_tokens: int, temperature: float) -> str:
        cmd = [
            ".\\libraries\\LlamaCpp_Binaries\\llama-cli.exe",
            "-m", self.model_path,
            "-p", prompt,
            "--temp", str(temperature),
            "-n", str(max_tokens),
            "-t", str(self.n_threads),
            "--ctx_size", str(cfg.context_size),
            "-ngl", "1"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def create_chat_completion(self, messages: List[Dict[str, str]], temperature: float = cfg.temperature, max_tokens: int = None) -> str:
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        return self.run_llama_cli(prompt, max_tokens or cfg.max_tokens, temperature)

class JsonHandler:
    @staticmethod
    def fix_and_parse_json(json_str: str) -> Union[str, Dict[Any, Any]]:
        try:
            json_str = json_str.replace('\t', '')
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Try to fix common JSON errors
            json_str = JsonHandler.correct_json(json_str)
            return json.loads(json_str)

    @staticmethod
    def correct_json(json_str: str) -> str:
        # Add quotes to property names
        json_str = re.sub(r'(\w+)(?=:)', r'"\1"', json_str)
        
        # Balance braces
        open_braces = json_str.count('{')
        close_braces = json_str.count('}')
        if open_braces > close_braces:
            json_str += '}' * (open_braces - close_braces)
        elif close_braces > open_braces:
            json_str = json_str.rstrip('}')
            json_str += '}' * open_braces

        # Fix invalid escapes
        json_str = re.sub(r'\\([^"\/bfnrtu])', r'\1', json_str)

        return json_str

    @staticmethod
    def get_command(response: str) -> tuple:
        try:
            response_json = JsonHandler.fix_and_parse_json(response)

            if "command" not in response_json:
                return "Error:", "Missing 'command' object in JSON"

            command = response_json["command"]

            if "name" not in command:
                return "Error:", "Missing 'name' field in 'command' object"

            command_name = command["name"]
            arguments = command.get("args", {})

            return command_name, arguments
        except json.JSONDecodeError:
            return "Error:", "Invalid JSON"
        except Exception as e:
            return "Error:", str(e)

# Example usage
if __name__ == "__main__":
    # Initialize the LlamaModel
    llm = LlamaModel()

    # Test LlamaModel
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ]
    response = llm.create_chat_completion(messages)
    print("LlamaModel response:", response)

    # Test JsonHandler
    json_str = '{"command": {"name": "test", "args": {"key": "value"}}}'
    parsed_json = JsonHandler.fix_and_parse_json(json_str)
    print("Parsed JSON:", parsed_json)

    command_name, arguments = JsonHandler.get_command(json_str)
    print("Command name:", command_name)
    print("Arguments:", arguments)