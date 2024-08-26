import os
import yaml

class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'persistent_settings.yaml')
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)

        # General Settings
        self.execute_local_commands = config.get('execute_local_commands', 'Allow')
        self.ai_settings_file = config.get('ai_settings_file', 'ai_settings.yaml')
        self.speak_mode = config.get('speak_mode', False)

        # LLM Model Settings
        self.smart_llm_model = config.get('smart_llm_model', './models/YourModel.gguf')
        self.smart_token_limit = config.get('smart_token_limit', 8000)
        self.embed_dim = config.get('embed_dim', 1536)
        self.gpu_threads_used = config.get('gpu_threads_used', 1024)
        self.temperature = config.get('temperature', 1)

        # Browsing Settings
        self.browse_chunk_max_length = config.get('browse_chunk_max_length', 8192)
        self.browse_summary_max_token = config.get('browse_summary_max_token', 300)
        self.user_agent = config.get('user_agent', 'Mozilla/5.0')

        # Playwright Settings
        self.playwright_headless = config.get('playwright_headless', True)
        self.playwright_timeout = config.get('playwright_timeout', 30000)

        # AI Configuration
        self.ai_name = config.get('ai_name', '')
        self.ai_role = config.get('ai_role', '')
        self.ai_goals = config.get('ai_goals', [])

        # Memory Settings
        self.memory_backend = config.get('memory_backend', 'local')
        self.memory_index = config.get('memory_index', 'autogpt-cppvulkan')

        # Debug Settings
        self.debug_mode = config.get('debug_mode', False)

        # Continuous Mode Settings
        self.continuous_mode = config.get('continuous_mode', False)
        self.continuous_limit = config.get('continuous_limit', 0)

        # Context Settings
        self.context_size = config.get('context_size', 8192)
        self.max_tokens = config.get('max_tokens', 4000)

        # File Paths
        self.model_path = config.get('model_path', './models')

    def save_config(self):
        config = {
            'execute_local_commands': self.execute_local_commands,
            'ai_settings_file': self.ai_settings_file,
            'speak_mode': self.speak_mode,
            'smart_llm_model': self.smart_llm_model,
            'smart_token_limit': self.smart_token_limit,
            'embed_dim': self.embed_dim,
            'gpu_threads_used': self.gpu_threads_used,
            'temperature': self.temperature,
            'browse_chunk_max_length': self.browse_chunk_max_length,
            'browse_summary_max_token': self.browse_summary_max_token,
            'user_agent': self.user_agent,
            'playwright_headless': self.playwright_headless,
            'playwright_timeout': self.playwright_timeout,
            'ai_name': self.ai_name,
            'ai_role': self.ai_role,
            'ai_goals': self.ai_goals,
            'memory_backend': self.memory_backend,
            'memory_index': self.memory_index,
            'debug_mode': self.debug_mode,
            'continuous_mode': self.continuous_mode,
            'continuous_limit': self.continuous_limit,
            'context_size': self.context_size,
            'max_tokens': self.max_tokens,
            'model_path': self.model_path,
        }

        with open(self.config_file, 'w') as file:
            yaml.dump(config, file)

    def set_continuous_mode(self, value: bool):
        self.continuous_mode = value
        self.save_config()

    def set_continuous_limit(self, value: int):
        self.continuous_limit = value
        self.save_config()

    def set_speak_mode(self, value: bool):
        self.speak_mode = value
        self.save_config()

    def set_debug_mode(self, value: bool):
        self.debug_mode = value
        self.save_config()