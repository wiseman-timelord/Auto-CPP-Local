import json
import random
import commands as cmd
import utils
from memory import get_memory, get_supported_memory_backends
import chat
from spinner import Spinner
import time
import speak
from config import Config
from json_parser import fix_and_parse_json
from ai_config import AIConfig
import traceback
import yaml
import argparse
from logger import logger
import logging
from prompt import get_prompt
from llm_utils import initialize_model, create_chat_completion

cfg = Config()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('--continuous', '-c', action='store_true', help='Enable Continuous Mode')
    parser.add_argument('--continuous-limit', '-l', type=int, dest="continuous_limit", help='Defines the number of times to run in continuous mode')
    parser.add_argument('--speak', action='store_true', help='Enable Speak Mode')
    parser.add_argument('--debug', action='store_true', help='Enable Debug Mode')
    parser.add_argument('--use-memory', '-m', dest="memory_type", help='Defines which Memory backend to use')
    parser.add_argument('--skip-reprompt', '-y', dest='skip_reprompt', action='store_true', help='Skips the re-prompting messages at the beginning of the script')
    parser.add_argument('--ai-settings', '-C', dest='ai_settings_file', help="Specifies which ai_settings.yaml file to use, will also automatically skip the re-prompt.")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.continuous:
        cfg.set_continuous_mode(True)
        cfg.set_continuous_limit(args.continuous_limit)
    if args.speak:
        cfg.set_speak_mode(True)
    if args.use_memory:
        cfg.memory_backend = args.use_memory
    if args.ai_settings_file:
        cfg.ai_settings_file = args.ai_settings_file
        cfg.skip_reprompt = True

def main():
    parse_arguments()
    logger.set_level(logging.DEBUG if cfg.debug_mode else logging.INFO)
    
    initialize_model()
    
    ai_name = ""
    prompt = construct_prompt()
    full_message_history = []
    next_action_count = 0
    user_input = "Determine which next command to use, and respond using the format specified above:"
    
    memory = get_memory(cfg, init=True)
    print('Using memory of type: ' + memory.__class__.__name__)
    
    agent = Agent(ai_name, memory, full_message_history, next_action_count, prompt, user_input)
    agent.start_interaction_loop()

class Agent:
    def __init__(self, ai_name, memory, full_message_history, next_action_count, prompt, user_input):
        self.ai_name = ai_name
        self.memory = memory
        self.full_message_history = full_message_history
        self.next_action_count = next_action_count
        self.prompt = prompt
        self.user_input = user_input

    def start_interaction_loop(self):
        loop_count = 0
        while True:
            loop_count += 1
            if cfg.continuous_mode and cfg.continuous_limit > 0 and loop_count > cfg.continuous_limit:
                logger.typewriter_log("Continuous Limit Reached: ", Fore.YELLOW, f"{cfg.continuous_limit}")
                break

            # Send message to AI, get response
            with Spinner("Thinking... "):
                assistant_reply = create_chat_completion(
                    messages=[{"role": "user", "content": self.prompt + "\n" + self.user_input}],
                    max_tokens=cfg.max_tokens
                )

            # Print Assistant thoughts
            print_assistant_thoughts(assistant_reply)

            # Get command name and arguments
            try:
                command_name, arguments = cmd.get_command(fix_and_parse_json(assistant_reply))
                if cfg.speak_mode:
                    speak.say_text(f"I want to execute {command_name}")
            except Exception as e:
                logger.error("Error: \n", str(e))

            if not cfg.continuous_mode and self.next_action_count == 0:
                ### GET USER AUTHORIZATION TO EXECUTE COMMAND ###
                # Get key press: Prompt the user to press enter to continue or escape
                # to exit
                self.user_input = ""
                logger.typewriter_log(
                    "NEXT ACTION: ",
                    "",
                    f"COMMAND = {command_name}  ARGUMENTS = {arguments}")
                print(
                    f"Enter 'y' to authorise command, 'y -N' to run N continuous commands, 'n' to exit program, or enter feedback for {self.ai_name}...",
                    flush=True)
                while True:
                    console_input = utils.clean_input(Fore.MAGENTA + "Input:" + Style.RESET_ALL)
                    if console_input.lower().rstrip() == "y":
                        self.user_input = "GENERATE NEXT COMMAND JSON"
                        break
                    elif console_input.lower().startswith("y -"):
                        try:
                            self.next_action_count = abs(int(console_input.split(" ")[1]))
                            self.user_input = "GENERATE NEXT COMMAND JSON"
                        except ValueError:
                            print("Invalid input format. Please enter 'y -n' where n is the number of continuous tasks.")
                            continue
                        break
                    elif console_input.lower() == "n":
                        self.user_input = "EXIT"
                        break
                    else:
                        self.user_input = console_input
                        command_name = "human_feedback"
                        break

                if self.user_input == "GENERATE NEXT COMMAND JSON":
                    logger.typewriter_log(
                        "-=-=-=-=-=-=-= COMMAND AUTHORISED BY USER -=-=-=-=-=-=-=",
                        Fore.MAGENTA,
                        "")
                elif self.user_input == "EXIT":
                    print("Exiting...", flush=True)
                    break
            else:
                # Print command
                logger.typewriter_log(
                    "NEXT ACTION: ",
                    Fore.CYAN,
                    f"COMMAND = {Fore.CYAN}{command_name}{Style.RESET_ALL}  ARGUMENTS = {Fore.CYAN}{arguments}{Style.RESET_ALL}")

            # Execute command
            if command_name.lower() != "human_feedback":
                result = f"Command {command_name} returned: {cmd.execute_command(command_name, arguments)}"
                if self.next_action_count > 0:
                    self.next_action_count -= 1
            else:
                result = f"Human feedback: {self.user_input}"

            memory_to_add = f"Assistant Reply: {assistant_reply} " \
                            f"\nResult: {result} " \
                            f"\nHuman Feedback: {self.user_input} "

            self.memory.add(memory_to_add)

            # Check if there's a result from the command append it to the message
            # history
            if result is not None:
                self.full_message_history.append(chat.create