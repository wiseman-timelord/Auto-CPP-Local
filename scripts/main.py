# Updated `.\scripts\main.py`

# Imports
import json, random, time, traceback, yaml, argparse, logging
from scripts.utilities import get_memory, logger, clean_input
from scripts.config import Config
from scripts.models import LlamaModel, JsonHandler
from scripts.prompt import get_prompt, chat_with_ai
from scripts.operations import execute_command

cfg = Config()

# Functions
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process args.')
    parser.add_argument('-c', '--continuous', action='store_true', help='Enable Continuous Mode')
    parser.add_argument('-l', '--continuous-limit', type=int, help='Set continuous run limit')
    parser.add_argument('--speak', action='store_true', help='Enable Speak Mode')
    parser.add_argument('--debug', action='store_true', help='Enable Debug Mode')
    parser.add_argument('-y', '--skip-reprompt', action='store_true', help='Skip reprompt messages')
    parser.add_argument('-C', '--config', help="Specify config file path")
    args = parser.parse_args()

    if args.config:
        cfg.config_file = args.config
        cfg.load_config()
    if args.continuous:
        cfg.program_settings['continuous_mode'] = True
    if args.continuous_limit is not None:
        cfg.program_settings['continuous_limit'] = args.continuous_limit
    if args.speak:
        cfg.system_settings['speak_mode'] = True
    if args.debug:
        cfg.program_settings['debug_mode'] = True

    return cfg

def main():
    cfg = parse_arguments()
    logger.set_level(logging.DEBUG if cfg.program_settings['debug_mode'] else logging.INFO)

    initialize_model(cfg)

    ai_name = cfg.session_settings.get('ai_name', 'AutoCPP-Lite')
    prompt = get_prompt()
    full_message_history, next_action_count = [], 0

    print(f"\nWelcome to AutoCPP-Lite. Using AI: {ai_name}")

    agent = Agent(ai_name, get_memory(cfg), full_message_history, next_action_count, prompt)
    agent.start_interaction_loop()

# Classes
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

# Entry Point
if __name__ == "__main__":
    main()