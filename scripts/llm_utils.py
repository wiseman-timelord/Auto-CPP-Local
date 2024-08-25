import subprocess
import os
import math
from config import Config

cfg = Config()

model_path = None
n_threads = None

def calculate_optimal_threads():
    total_threads = os.cpu_count() or 4
    return math.ceil((total_threads / 100) * 85)

def initialize_model():
    global model_path, n_threads
    model_dir = cfg.model_path
    for file in os.listdir(model_dir):
        if file.endswith(".gguf"):
            model_path = os.path.join(model_dir, file)
            break
    
    if model_path is None:
        raise FileNotFoundError(f"No .gguf model found in {model_dir}")

    n_threads = calculate_optimal_threads()
    total_threads = os.cpu_count() or 4
    thread_usage_percentage = (n_threads / total_threads) * 100
    print(f"\nModel initialized: {model_path}")
    print(f"Using {n_threads} threads ({thread_usage_percentage:.2f}% of available CPU threads).")

def run_llama_cli(prompt, max_tokens, temperature):
    cmd = [
        ".\\libraries\\LlamaCpp_Binaries\\llama-cli.exe",
        "-m", model_path,
        "-p", prompt,
        "--temp", str(temperature),
        "-n", str(max_tokens),
        "-t", str(n_threads),
        "--ctx_size", str(cfg.context_size),
        "-ngl", "1"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout

def create_chat_completion(messages, model=None, temperature=cfg.temperature, max_tokens=None) -> str:
    prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
    return run_llama_cli(prompt, max_tokens or cfg.max_tokens, temperature)