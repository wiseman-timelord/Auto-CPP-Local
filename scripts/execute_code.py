import os
import subprocess

WORKSPACE_FOLDER = ".\workspace"

def execute_python_file(file):
    """Execute a Python file and return the output"""
    print(f"Executing file '{file}' in workspace '{WORKSPACE_FOLDER}'")

    if not file.endswith(".py"):
        return "Error: Invalid file type. Only .py files are allowed."

    file_path = os.path.join(WORKSPACE_FOLDER, file)

    if not os.path.isfile(file_path):
        return f"Error: File '{file}' does not exist."

    try:
        result = subprocess.run(['python', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def execute_shell(command_line):

    current_dir = os.getcwd()

    if not WORKSPACE_FOLDER in current_dir: # Change dir into workspace if necessary
        work_dir = os.path.join(os.getcwd(), WORKSPACE_FOLDER)
        os.chdir(work_dir)

    print (f"Executing command '{command_line}' in working directory '{os.getcwd()}'")

    result = subprocess.run(command_line, capture_output=True, shell=True)
    output = f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

    # Change back to whatever the prior working dir was

    os.chdir(current_dir)

    return output


def we_are_running_in_a_docker_container():
    os.path.exists('/.dockerenv')
