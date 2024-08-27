# `.\scripts\main.py`

# Imports
import json, random, time, traceback, yaml, argparse, logging
from utilities import get_memory, logger, say_text, clean_input
from config import Config
from models import create_chat_completion, fix_json
from prompt import get_prompt, generate_context, chat_with_ai
from operations import execute_command, web_search, get_datetime, browse_website, get_text_summary, get_hyperlinks, commit_memory, delete_memory, overwrite_memory, shutdown, start_agent, message_agent, list_agents, delete_agent
from llm_utilities import initialize_model

cfg = Config()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process args.')
    parser.add_argument('-c', '--continuous', action='store_true', help='Enable Continuous Mode')
    parser.add_argument('-l', '--continuous-limit', type=int, help='Set continuous run limit')
    parser.add_argument('--speak', action='store_true', help='Enable Speak Mode')
    parser.add_argument('--debug', action='store_true', help='Enable Debug Mode')
    parser.add_argument('-y', '--skip-reprompt', action='store_true', help='Skip reprompt messages')
    parser.add_argument('-C', '--config', help="Specify config file path")
    args = parser.parse_args()

    cfg = Config()
    if args.config:
        cfg.config_file = args.config
        cfg.load_config()
    if args.continuous:
        cfg.set_continuous_mode(True)
    if args.continuous_limit is not None:
        cfg.set_continuous_limit(args.continuous_limit)
    if args.speak:
        cfg.set_speak_mode(True)
    if args.debug:
        cfg.set_debug_mode(True)

    return cfg

# Update the main function to use the new Config
def main():
    cfg = parse_arguments()
    logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)
    
    initialize_model(cfg)
    
    ai_name = cfg.session_settings.get('ai_name', 'AutoCPP-Lite')
    prompt = get_prompt()
    full_message_history, next_action_count = [], 0
    
    print(f"\nWelcome to AutoCPP-Lite. Using AI: {ai_name}")
    
    agent = Agent(ai_name, get_memory(cfg), full_message_history, next_action_count, prompt)
    agent.start_interaction_loop()

class Agent:
    def __init__(self, ai_name, memory, full_message_history, next_action_count, prompt):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.prompt = prompt
        self.user_input = "Determine which next command to use, and respond using the JSON format specified above:"

    def start_interaction_loop(self):
        cfg = Config()
        loop_count = 0
        while True:
            loop_count += 1
            if cfg.continuous_mode and cfg.continuous_limit > 0 and loop_count > cfg.continuous_limit:
                logger.typewriter_log("Continuous Limit Reached: ", Fore.YELLOW, f"{cfg.continuous_limit}")
                break

            # Send message to AI, get response
            assistant_reply = chat_with_ai(
                self.prompt,
                self.user_input,
                self.full_message_history,
                self.memory,
                cfg.llm_model_settings['smart_token_limit']
            )

            # Print Assistant thoughts
            print_assistant_thoughts(assistant_reply)

            # Get command name and arguments
            try:
                command = json.loads(assistant_reply)
                command_name = command["command"]["name"]
                arguments = command["command"]["args"]
                
                # Execute command
                if cfg.system_settings['speak_mode']:
                    say_text(f"I want to execute {command_name}")
                
                result = execute_command(command_name, arguments)
                
                if result is not None:
                    self.memory.add(f"Command {command_name} returned: {result}")

                # Check if there's a result from the command append it to the message
                # history
                if result is not None:
                    self.full_message_history.append(
                        create_chat_message("system", f"Command {command_name} returned: {result}"))
                else:
                    self.full_message_history.append(
                        create_chat_message("system", f"Command {command_name} executed successfully."))

            except json.decoder.JSONDecodeError:
                logger.error("Error: Invalid JSON in assistant reply")
                self.full_message_history.append(create_chat_message("system", "Error: Invalid JSON in assistant reply"))
            
            except Exception as e:
                logger.error(f"Error: {str(e)}")

            # Check if there's a user input needed
            if not cfg.continuous_mode and self.next_action_count == 0:
                self.user_input = clean_input(f"Human feedback: ")
                if self.user_input.lower().strip() == "exit":
                    print("Exiting...")
                    break
            else:
                print("Continuing...")
            
            self.memory.add(f"Human feedback: {self.user_input}")
            self.full_message_history.append(create_chat_message("human", self.user_input))

def handle_user_input(command_name, arguments):
    print(f"Authorize command: {command_name} {arguments}? (y/n)", flush=True)
    while True:
        console_input = clean_input("Input: ").lower().strip()
        if console_input == "y":
            return "GENERATE NEXT COMMAND JSON"
        elif console_input.startswith("y -"):
            try:
                self.next_action_count = abs(int(console_input.split(" ")[1]))
                return "GENERATE NEXT COMMAND JSON"
            except ValueError:
                print("Invalid input. Use 'y -n' for continuous.")
        elif console_input == "n":
            return "EXIT"
        elif command_name.lower() == "web_search":
            search_results = web_search(arguments.get("query", ""))
            print(f"Search Results: {search_results}")
        else:
            return console_input


def log_command(command_name, arguments):
    logger.typewriter_log("NEXT ACTION: ", "", f"COMMAND = {command_name} ARGUMENTS = {arguments}")

def print_assistant_thoughts(assistant_reply):
    logger.typewriter_log("Assistant Thoughts: ", "", assistant_reply)
