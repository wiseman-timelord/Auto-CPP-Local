import os, yaml
from dotenv import load_dotenv
from prompt import get_prompt

load_dotenv()

class AIConfig:
    """
    A class object that contains the configuration information for the AI

    Attributes:
        ai_name (str): The name of the AI.
        ai_role (str): The description of the AI's role.
        ai_goals (list): The list of objectives the AI is supposed to complete.
    """

    def __init__(self, ai_name: str="", ai_role: str="", ai_goals: list=[]) -> None:
        """
        Initialize a class instance

        Parameters:
            ai_name (str): The name of the AI.
            ai_role (str): The description of the AI's role.
            ai_goals (list): The list of objectives the AI is supposed to complete.
        Returns:
            None
        """

        self.ai_name = ai_name
        self.ai_role = ai_role
        self.ai_goals = ai_goals

    # Soon this will go in a folder where it remembers more stuff about the run(s)
    SAVE_FILE = os.path.join(os.path.dirname(__file__), '..', 'ai_settings.yaml')

    @classmethod
    def load(cls: object, config_file: str=SAVE_FILE) -> object:
        """
        Returns class object with parameters (ai_name, ai_role, ai_goals) loaded from yaml file if yaml file exists,
        else returns class with no parameters.

        Parameters:
           cls (class object): An AIConfig Class object.
           config_file (int): The path to the config yaml file. DEFAULT: "../ai_settings.yaml"

        Returns:
            cls (object): An instance of given cls object
        """

        try:
            with open(config_file, encoding='utf-8') as file:
                config_params = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            config_params = {}

        ai_name = config_params.get("ai_name", "")
        ai_role = config_params.get("ai_role", "")
        ai_goals = config_params.get("ai_goals", [])

        return cls(ai_name, ai_role, ai_goals)

    def save(self, config_file: str=SAVE_FILE) -> None:
        """
        Saves the class parameters to the specified file yaml file path as a yaml file.

        Parameters:
            config_file(str): The path to the config yaml file. DEFAULT: "../ai_settings.yaml"

        Returns:
            None
        """

        config = {"ai_name": self.ai_name, "ai_role": self.ai_role, "ai_goals": self.ai_goals}
        with open(config_file, "w",  encoding='utf-8') as file:
            yaml.dump(config, file, allow_unicode=True)

    def construct_full_prompt(self) -> str:
        """
        Returns a prompt to the user with the class information in an organized fashion.

        Parameters:
            None

        Returns:
            full_prompt (str): A string containing the initial prompt for the user including the ai_name, ai_role and ai_goals.
        """

        prompt_start = """Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications."""

        # Construct full prompt
        full_prompt = f"You are {self.ai_name}, {self.ai_role}\n{prompt_start}\n\nGOALS:\n\n"
        for i, goal in enumerate(self.ai_goals):
            full_prompt += f"{i+1}. {goal}\n"

        full_prompt += f"\n\n{get_prompt()}"
        return full_prompt

class Config:
    def __init__(self):
        self.debug_mode = False
        self.continuous_mode = False
        self.continuous_limit = 0
        self.speak_mode = False
        self.skip_reprompt = False

        self.ai_settings_file = os.getenv("AI_SETTINGS_FILE", "ai_settings.yaml")
        self.model_path = os.getenv("MODEL_PATH", "./models")
        self.context_size = int(os.getenv("CONTEXT_SIZE", "8192"))
        self.embed_dim = int(os.getenv("EMBED_DIM", 4096))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.5"))

        self.memory_backend = 'local'  # Default to local memory
        self.memory_index = os.getenv("MEMORY_INDEX", 'autogpt-cppvulkan')

    def set_continuous_mode(self, value: bool):
        self.continuous_mode = value

    def set_continuous_limit(self, value: int):
        self.continuous_limit = value

    def set_speak_mode(self, value: bool):
        self.speak_mode = value

    def set_debug_mode(self, value: bool):
        self.debug_mode = value
