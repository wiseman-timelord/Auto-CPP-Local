# `.\scripts\prompt.py`

# Imports
import json, time
from utilities import LocalCache
from config import Config
import models
from models import create_chat_completion
from utilities import logger

cfg = Config()
permanent_memory = LocalCache(cfg)

class PromptGenerator:
    """
    A class for generating custom prompt strings based on constraints, commands, resources, and performance evaluations.
    """

    def __init__(self):
        """
        Initialize the PromptGenerator object with empty lists of constraints, commands, resources, and performance evaluations.
        """
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
        """
        Add a constraint to the constraints list.

        Args:
            constraint (str): The constraint to be added.
        """
        self.constraints.append(constraint)

    def add_command(self, command_label, command_name, args=None):
        """
        Add a command to the commands list with a label, name, and optional arguments.

        Args:
            command_label (str): The label of the command.
            command_name (str): The name of the command.
            args (dict, optional): A dictionary containing argument names and their values. Defaults to None.
        """
        if args is None:
            args = {}

        command_args = {arg_key: arg_value for arg_key,
                        arg_value in args.items()}

        command = {
            "label": command_label,
            "name": command_name,
            "args": command_args,
        }

        self.commands.append(command)

    def _generate_command_string(self, command):
        """
        Generate a formatted string representation of a command.

        Args:
            command (dict): A dictionary containing command information.

        Returns:
            str: The formatted command string.
        """
        args_string = ', '.join(
            f'"{key}": "{value}"' for key, value in command['args'].items())
        return f'{command["label"]}: "{command["name"]}", args: {args_string}'

    def add_resource(self, resource):
        """
        Add a resource to the resources list.

        Args:
            resource (str): The resource to be added.
        """
        self.resources.append(resource)

    def add_performance_evaluation(self, evaluation):
        """
        Add a performance evaluation item to the performance_evaluation list.

        Args:
            evaluation (str): The evaluation item to be added.
        """
        self.performance_evaluation.append(evaluation)

    def _generate_numbered_list(self, items, item_type='list'):
        """
        Generate a numbered list from given items based on the item_type.

        Args:
            items (list): A list of items to be numbered.
            item_type (str, optional): The type of items in the list. Defaults to 'list'.

        Returns:
            str: The formatted numbered list.
        """
        if item_type == 'command':
            return "\n".join(f"{i+1}. {self._generate_command_string(item)}" for i, item in enumerate(items))
        else:
            return "\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

    def generate_prompt_string(self):
        """
        Generate a prompt string based on the constraints, commands, resources, and performance evaluations.

        Returns:
            str: The generated prompt string.
        """
        formatted_response_format = json.dumps(self.response_format, indent=4)
        prompt_string = (
            f"Constraints:\n{self._generate_numbered_list(self.constraints)}\n\n"
            f"Commands:\n{self._generate_numbered_list(self.commands, item_type='command')}\n\n"
            f"Resources:\n{self._generate_numbered_list(self.resources)}\n\n"
            f"Performance Evaluation:\n{self._generate_numbered_list(self.performance_evaluation)}\n\n"
            f"You should only respond in JSON format as described below \nResponse Format: \n{formatted_response_format} \nEnsure the response can be parsed by Python json.loads"
        )

        return prompt_string

def create_chat_message(role, content):
    return {"role": role, "content": content}
    
def generate_context(prompt, relevant_memory, full_message_history):
    current_context = [
        create_chat_message("system", prompt),
        create_chat_message("system", f"The current time and date is {time.strftime('%c')}"),
        create_chat_message("system", f"This reminds you of these events from your past:\n{relevant_memory}\n\n")]

    # Add messages from the full message history until we reach the token limit
    next_message_to_add_index = len(full_message_history) - 1
    insertion_index = len(current_context)
    current_tokens_used = models.count_message_tokens(current_context)
    return next_message_to_add_index, current_tokens_used, insertion_index, current_context
    
def chat_with_ai(prompt, user_input, full_message_history, permanent_memory, token_limit):
    while True:
        try:
            send_token_limit = token_limit - 1000
            relevant_memory = '' if len(full_message_history) == 0 else permanent_memory.get_relevant(str(full_message_history[-9:]), 10)

            next_message_to_add_index, current_tokens_used, insertion_index, current_context = generate_context(
                prompt, relevant_memory, full_message_history)

            while current_tokens_used > 2500:
                relevant_memory = relevant_memory[1:]
                next_message_to_add_index, current_tokens_used, insertion_index, current_context = generate_context(
                    prompt, relevant_memory, full_message_history)

            current_tokens_used += models.count_message_tokens([create_chat_message("user", user_input)])

            while next_message_to_add_index >= 0:
                message_to_add = full_message_history[next_message_to_add_index]
                tokens_to_add = models.count_message_tokens([message_to_add])
                if current_tokens_used + tokens_to_add > send_token_limit:
                    break
                current_context.insert(insertion_index, full_message_history[next_message_to_add_index])
                current_tokens_used += tokens_to_add
                next_message_to_add_index -= 1

            current_context.extend([create_chat_message("user", user_input)])

            tokens_remaining = token_limit - current_tokens_used

            assistant_reply = create_chat_completion(
                messages=current_context,
                max_tokens=tokens_remaining,
            )

            full_message_history.append(create_chat_message("user", user_input))
            full_message_history.append(create_chat_message("assistant", assistant_reply))

            return assistant_reply
        except Exception as e:
            logger.error(f"Error: {str(e)}")
            time.sleep(10)
    
def get_prompt():
    """
    This function generates a prompt string that includes various constraints, commands, resources, and performance evaluations.

    Returns:
        str: The generated prompt string.
    """

    # Initialize the PromptGenerator object
    prompt_generator = PromptGenerator()

    # Add constraints to the PromptGenerator object
    prompt_generator.add_constraint("~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.")
    prompt_generator.add_constraint("If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.")
    prompt_generator.add_constraint("No user assistance")
    prompt_generator.add_constraint('Exclusively use the commands listed in double quotes e.g. "command name"')

    # Define the command list
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
        ("Execute Shell Command, non-interactive commands only", "execute_shell", { "command_line": "<command_line>"}),
        ("Task Complete (Shutdown)", "task_complete", {"reason": "<reason>"}),
        ("Do Nothing", "do_nothing", {}),
    ]

    # Add commands to the PromptGenerator object
    for command_label, command_name, args in commands:
        prompt_generator.add_command(command_label, command_name, args)

    # Add resources to the PromptGenerator object
    prompt_generator.add_resource("Internet access for searches and information gathering.")
    prompt_generator.add_resource("Long Term memory management.")
    prompt_generator.add_resource("GPT-3.5 powered Agents for delegation of simple tasks.")
    prompt_generator.add_resource("File output.")

    # Add performance evaluations to the PromptGenerator object
    prompt_generator.add_performance_evaluation("Continuously review and analyze your actions to ensure you are performing to the best of your abilities.")
    prompt_generator.add_performance_evaluation("Constructively self-criticize your big-picture behavior constantly.")
    prompt_generator.add_performance_evaluation("Reflect on past decisions and strategies to refine your approach.")
    prompt_generator.add_performance_evaluation("Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.")

    # Generate the prompt string
    prompt_string = prompt_generator.generate_prompt_string()

    return prompt_string