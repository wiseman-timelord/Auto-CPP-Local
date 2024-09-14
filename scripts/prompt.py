# `.\scripts\prompt.py`

# Imports
import json, time
from scripts.utilities import LocalCache, logger
from scripts.config import Config
from scripts.models import LlamaModel, JsonHandler

# Globals
cfg = Config()
permanent_memory = LocalCache(cfg)

# Classes
class PromptGenerator:
    def __init__(self):
        self.constraints = []
        self.commands = []
        self.resources = []
        self.performance_evaluation = []
        self.response_format = {
            "thoughts": {
                "text": "thought",
                "reasoning": "reasoning",
                "plan": "- short bulleted\n- list that conveys\n- long-term plan",
                "criticism": "constructive self-criticism",
                "speak": "thoughts summary to say to user"
            },
            "command": {
                "name": "command name",
                "args": {
                    "arg name": "value"
                }
            }
        }

    def add_constraint(self, constraint):
        if isinstance(constraint, str) and constraint:
            self.constraints.append(constraint)
        else:
            logger.warn(f"Invalid constraint format: {constraint}")

    def add_command(self, command_label, command_name, args=None):
        if args is None:
            args = {}

        if not isinstance(command_label, str) or not isinstance(command_name, str):
            logger.warn(f"Invalid command format: {command_label}, {command_name}")
            return

        command_args = {arg_key: arg_value for arg_key, arg_value in args.items() if isinstance(arg_key, str) and isinstance(arg_value, str)}
        command = {"label": command_label, "name": command_name, "args": command_args}
        self.commands.append(command)

    def _generate_command_string(self, command):
        def format_args(args):
            return ', '.join(f'"{key}": "{value}"' if not isinstance(value, dict) else f'"{key}": {{{format_args(value)}}}' for key, value in args.items())
        return f'{command["label"]}: "{command["name"]}", args: {format_args(command["args"])}'

    def add_resource(self, resource):
        if isinstance(resource, str) and resource:
            self.resources.append(resource)
        else:
            logger.warn(f"Invalid resource format: {resource}")

    def add_performance_evaluation(self, evaluation):
        if isinstance(evaluation, str) and evaluation:
            self.performance_evaluation.append(evaluation)
        else:
            logger.warn(f"Invalid performance evaluation format: {evaluation}")

    def _generate_numbered_list(self, items, item_type='list'):
        if item_type == 'command':
            return "\n".join(f"{i+1}. {self._generate_command_string(item)}" for i, item in enumerate(items))
        else:
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def generate_prompt_string(self):
        formatted_response_format = json.dumps(self.response_format, indent=4)
        prompt_string = (
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
            f"Commands:\n{self._generate_numbered_list(self.commands, item_type='command')}\n\n"
            f"Resources:\n{self._generate_numbered_list(self.resources)}\n\n"
            f"Performance Evaluation:\n{self._generate_numbered_list(self.performance_evaluation)}\n\n"
            f"You should only respond in JSON format as described below \nResponse Format: \n{formatted_response_format} \nEnsure the response can be parsed by Python json.loads"
        )
        return prompt_string

# Functions
def create_chat_message(role, content):
    return {"role": role, "content": content}

def generate_context(prompt, relevant_memory, full_message_history):
    try:
        current_context = [
            create_chat_message("system", prompt),
            create_chat_message("system", f"The current time and date is {time.strftime('%c')}"),
            create_chat_message("system", f"This reminds you of these events from your past:\n{relevant_memory}\n\n")
        ]
        next_message_to_add_index = len(full_message_history) - 1
        insertion_index = len(current_context)
        current_tokens_used = LlamaModel.count_message_tokens(current_context)
        return next_message_to_add_index, current_tokens_used, insertion_index, current_context
    except Exception as e:
        logger.error(f"Error generating context: {str(e)}")
        return 0, 0, 0, []

def chat_with_ai(prompt, user_input, full_message_history, permanent_memory, token_limit):
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            send_token_limit = token_limit - 1000
            relevant_memory = '' if len(full_message_history) == 0 else permanent_memory.get_relevant(str(full_message_history[-9:]), 10)

            next_message_to_add_index, current_tokens_used, insertion_index, current_context = generate_context(
                prompt, relevant_memory, full_message_history)

            while current_tokens_used > 2500:
                relevant_memory = relevant_memory[1:]
                next_message_to_add_index, current_tokens_used, insertion_index, current_context = generate_context(
                    prompt, relevant_memory, full_message_history)

            current_tokens_used += LlamaModel.count_message_tokens([create_chat_message("user", user_input)])

            while next_message_to_add_index >= 0:
                message_to_add = full_message_history[next_message_to_add_index]
                tokens_to_add = LlamaModel.count_message_tokens([message_to_add])
                if current_tokens_used + tokens_to_add > send_token_limit:
                    break
                current_context.insert(insertion_index, full_message_history[next_message_to_add_index])
                current_tokens_used += tokens_to_add
                next_message_to_add_index -= 1

            current_context.append(create_chat_message("user", user_input))
            tokens_remaining = token_limit - current_tokens_used

            assistant_reply = LlamaModel('chat').create_chat_completion(
                messages=current_context,
                max_tokens=tokens_remaining,
            )

            full_message_history.append(create_chat_message("user", user_input))
            full_message_history.append(create_chat_message("assistant", assistant_reply))

            return assistant_reply
        except Exception as e:
            logger.error(f"Error during AI chat interaction: {str(e)}")
            retry_count += 1
            time.sleep(10)

    logger.error("Max retries reached during chat interaction.")
    return "Error: Could not complete the chat interaction due to repeated errors."

    logger.error("Max retries reached during chat interaction.")
    return "Error: Could not complete the chat interaction due to repeated errors."

def get_prompt():
    prompt_generator = PromptGenerator()
    prompt_generator.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so make best use of System Memory.")
    prompt_generator.add_constraint("If you are unsure how you previously did something or want to recall past events, think about similar events.")
    prompt_generator.add_constraint("No user assistance, try to determine the best solutions, and act independently.")
    prompt_generator.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name".')

    commands = [
        ("Web Search", "web_search", {"query": "<search>"}),
        ("Browse Website", "browse_website", {"url": "<url>", "question": "<what_you_want_to_find_on_website>"}),
        ("Start GPT Agent", "start_agent", {"name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"}),
        ("Message GPT Agent", "message_agent", {"key": "<key>", "message": "<message>"}),
        ("List GPT Agents", "list_agents", {}),
        ("Delete GPT Agent", "delete_agent", {"key": "<key>"}),
        ("Write to file", "write_to_file", {"file": "<file>", "text": "<text>"}),
        ("Read file", "read_file", {"file": "<file>"}),
        ("Append to file", "append_to_file", {"file": "<file>", "text": "<text>"}),
        ("Delete file", "delete_file", {"file": "<file>"}),
        ("Search Files", "search_files", {"directory": "<directory>"}),
        ("Evaluate Code", "evaluate_code", {"code": "<full_code_string>"}),
        ("Get Improved Code", "improve_code", {"suggestions": "<list_of_suggestions>", "code": "<full_code_string>"}),
        ("Write Tests", "write_tests", {"code": "<full_code_string>", "focus": "<list_of_focus_areas>"}),
        ("Execute Python File", "execute_python_file", {"file": "<file>"}),
        ("Execute Shell Command", "execute_shell", {"command_line": "<command_line>"}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("Do Nothing", "do_nothing", {}),
    ]

    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    prompt_generator.add_resource("Internet access for information, searches and gathering.")
    prompt_generator.add_resource("Long Term memory management though system memory.")
    prompt_generator.add_resource("8k Local Model powered Agents for delegation of tasks.")
    prompt_generator.add_resource("File output for backing up and saving.")

    prompt_generator.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to your best.")
    prompt_generator.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
    prompt_generator.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
    prompt_generator.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    return prompt_generator.generate_prompt_string()