import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    def __init__(self):
        self.debug_mode = False
        self.continuous_mode = False
        self.continuous_limit = 0
        self.speak_mode = False
        self.skip_reprompt = False

        self.ai_settings_file = os.getenv("AI_SETTINGS_FILE", "ai_settings.yaml")
        self.model_path = os.getenv("MODEL_PATH", "./models")
        self.context_size = int(os.getenv("CONTEXT_SIZE", "2048"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

        self.memory_backend = os.getenv("MEMORY_BACKEND", 'local')
        self.memory_index = os.getenv("MEMORY_INDEX", 'auto-gpt')

    def set_continuous_mode(self, value: bool):
        self.continuous_mode = value

    def set_continuous_limit(self, value: int):
        self.continuous_limit = value

    def set_speak_mode(self, value: bool):
        self.speak_mode = value

    def set_debug_mode(self, value: bool):
        self.debug_mode = value