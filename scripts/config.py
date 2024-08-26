import os
import yaml

class Config:
    def __init__(self):
        self.config_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'persistent_settings.yaml')
        self.load_config()

    def load_config(self):
        with open(self.config_file, 'r') as file:
            config = yaml.safe_load(file)

        # Splitting settings into categories
        self.program_settings = {
            'execute_local_commands': config.get('execute_local_commands', 'Allow'),
            'continuous_mode': config.get('continuous_mode', False),
            'continuous_limit': config.get('continuous_limit', 0),
            'debug_mode': config.get('debug_mode', False)
        }

        self.session_settings = {
            'ai_settings_file': config.get('ai_settings_file', 'ai_settings.yaml'),
            'user_name': config.get('user_name', ''),
            'ai_name': config.get('ai_name', ''),
            'ai_role': config.get('ai_role', ''),
            'ai_goals': config.get('ai_goals', [])
        }

        self.system_settings = {
            'memory_backend': config.get('memory_backend', 'local'),
            'memory_index': config.get('memory_index', 'autoccp-lite'),
            'speak_mode': config.get('speak_mode', False)
        }

        self.llm_model_settings = {
            'model_path': config.get('model_path', './models'),
            'smart_llm_model': config.get('smart_llm_model', './models/YourModel.gguf'),
            'context_size': config.get('context_size', 8192),
            'max_tokens': config.get('max_tokens', 4000),
            'smart_token_limit': config.get('smart_token_limit', 8000),
            'embed_dim': config.get('embed_dim', 1536),
            'gpu_threads_used': config.get('gpu_threads_used', 1024),
            'temperature': config.get('temperature', 1)
        }

        self.browsing_settings = {
            'browse_chunk_max_length': config.get('browse_chunk_max_length', 8192),
            'browse_summary_max_token': config.get('browse_summary_max_token', 300),
            'user_agent': config.get('user_agent', 'Mozilla/5.0'),
            'playwright_headless': config.get('playwright_headless', True),
            'playwright_timeout': config.get('playwright_timeout', 30000)
        }

    def save_config(self):
        config = {**self.program_settings, **self.session_settings, **self.system_settings, 
                  **self.llm_model_settings, **self.browsing_settings}

        with open(self.config_file, 'w') as file:
            yaml.dump(config, file)
