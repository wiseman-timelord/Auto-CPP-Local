# Updated `.\scripts\main.py`

# Imports
import os
import time
import logging
from scripts.utilities import get_memory, logger, clean_input
from scripts.config import Config
from scripts.models import LlamaModel, JsonHandler
from scripts.prompt import get_prompt, chat_with_ai
from scripts.operations import execute_command

cfg = Config()

def clear_folders():
    folders_to_clear = [".\\cache\\downloads", ".\\cache\\working"]
    for folder in folders_to_clear:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

def main():
    logger.set_level(logging.DEBUG if cfg.program_settings['debug_mode'] else logging.INFO)

    chat_model = LlamaModel('chat')
    code_model = LlamaModel('code')

    ai_name = cfg.session_settings.get('ai_name', 'Auto-CPP-Local')
    prompt = get_prompt()
    full_message_history, next_action_count = [], 0

    print(f"\nWelcome to Auto-CPP-Local. Using AI: {ai_name}")

    agent = Agent(ai_name, get_memory(cfg), full_message_history, next_action_count, prompt)
    agent.start_interaction_loop()

class Agent:
    def __init__(self, ai_name, memory, full_message_history, next_action_count, prompt):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.prompt = prompt
        self.user_input = "Determine the next command to use, and respond using the JSON format specified."

    def start_interaction_loop(self):
        loop_count = 0
        while True:
            loop_count += 1
            if cfg.program_settings['continuous_mode'] and cfg.program_settings['continuous_limit'] > 0 and loop_count > cfg.program_settings['continuous_limit']:
                logger.typewriter_log("Continuous Limit Reached: ", "yellow", f"{cfg.program_settings['continuous_limit']}")
                break

            try:
                assistant_reply = chat_with_ai(
                    self.prompt,
                    self.user_input,
                    self.full_message_history,
                    self.memory,
                    cfg.llm_model_settings['smart_token_limit']
                )
                self.process_assistant_reply(assistant_reply)
            except Exception as e:
                logger.error(f"Error during interaction loop: {str(e)}")

            if not cfg.program_settings['continuous_mode']:
                self.user_input = clean_input("Human feedback: ")
                if self.user_input.lower().strip() == "exit":
                    print("Exiting...")
                    break
            else:
                print("Continuing...")

            self.memory.add(f"Human feedback: {self.user_input}")
            self.full_message_history.append(JsonHandler.create_chat_message("human", self.user_input))

    def process_assistant_reply(self, assistant_reply):
        command_name, arguments = JsonHandler.get_command(assistant_reply)
        if command_name == "Error":
            logger.error(f"Invalid command: {arguments}")
            return

        result = execute_command(command_name, arguments)

        if result is not None:
            self.memory.add(f"Command {command_name} returned: {result}")
            self.full_message_history.append(JsonHandler.create_chat_message("system", f"Command {command_name} returned: {result}"))
        else:
            self.full_message_history.append(JsonHandler.create_chat_message("system", f"Command {command_name} executed successfully."))

if __name__ == "__main__":
    clear_folders()  # Clear folders at the start of a new project
    main()