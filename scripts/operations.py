import os
import subprocess

WORKSPACE_FOLDER = ".\\workspace"

# Ensure workspace exists
os.makedirs(WORKSPACE_FOLDER, exist_ok=True)

def safe_join(base, *paths):
    """Safely join paths."""
    new_path = os.path.normpath(os.path.join(base, *paths))
    if os.path.commonprefix([base, new_path]) != base:
        raise ValueError("Path escape detected.")
    return new_path

def execute_shell(command_line):
    """Run shell command."""
    initial_dir = os.getcwd()
    os.chdir(WORKSPACE_FOLDER) if WORKSPACE_FOLDER not in initial_dir else None
    result = subprocess.run(command_line, capture_output=True, shell=True)
    os.chdir(initial_dir)
    return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def execute_python_file(file):
    """Run a Python file."""
    if not file.endswith(".py"):
        return "Error: Only .py files."
    file_path = os.path.join(WORKSPACE_FOLDER, file)
    if not os.path.isfile(file_path):
        return f"Error: File '{file}' not found."
    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def split_file(content, max_length=4000, overlap=0):
    """Split text into chunks."""
    for start in range(0, len(content), max_length - overlap):
        yield content[start:start + max_length]

def read_file(filename):
    """Read file contents."""
    try:
        with open(safe_join(WORKSPACE_FOLDER, filename), "r", encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"

def ingest_file(filename, memory, max_length=4000, overlap=200):
    """Ingest file into memory."""
    try:
        content = read_file(filename)
        for i, chunk in enumerate(split_file(content, max_length, overlap)):
            memory.add(f"File: {filename} | Part: {i + 1}\n{chunk}")
        return f"Ingested {filename}."
    except Exception as e:
        return f"Error ingesting '{filename}': {str(e)}"

def write_to_file(filename, text):
    """Write text to file."""
    try:
        filepath = safe_join(WORKSPACE_FOLDER, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(text)
        return "File written."
    except Exception as e:
        return f"Error: {str(e)}"

def append_to_file(filename, text):
    """Append text to file."""
    try:
        with open(safe_join(WORKSPACE_FOLDER, filename), "a", encoding='utf-8') as f:
            f.write(text)
        return "Text appended."
    except Exception as e:
        return f"Error: {str(e)}"

def delete_file(filename):
    """Delete file."""
    try:
        os.remove(safe_join(WORKSPACE_FOLDER, filename))
        return "File deleted."
    except Exception as e:
        return f"Error: {str(e)}"

def search_files(directory):
    """Search files in directory."""
    found_files = []
    search_dir = safe_join(WORKSPACE_FOLDER, directory or "")
    for root, _, files in os.walk(search_dir):
        for file in files:
            if not file.startswith('.'):
                found_files.append(os.path.relpath(os.path.join(root, file), WORKSPACE_FOLDER))
    return found_files
