# `.\scripts\utilities_two.py` The Utilities script to fix circular imports.

# Imports
import logging
import os
import random
import re
import time
import win32com.client
from scripts.config import Config

# Global Config
cfg = Config()
speaker = win32com.client.Dispatch("SAPI.SpVoice")

class AutoGptFormatter(logging.Formatter):
    def format(self, record):
        record.title_color = f"{getattr(record, 'title', '')} "
        record.message_no_color = remove_color_codes(getattr(record, 'msg', ''))
        return super().format(record)

class TypingConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        min_speed, max_speed = 0.05, 0.01
        msg = self.format(record)
        for word in msg.split():
            print(word, end=" ", flush=True)
            time.sleep(random.uniform(min_speed, max_speed))
            min_speed, max_speed = min_speed * 0.95, max_speed * 0.95
        print()

class ConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        print(self.format(record))

class Logger:
    def __init__(self):
        log_dir = os.path.join(os.path.dirname(__file__), '../logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "activity.log")
        error_file = os.path.join(log_dir, "error.log")

        console_formatter = AutoGptFormatter('%(title_color)s %(message)s')

        self.typing_console_handler = TypingConsoleHandler()
        self.console_handler = ConsoleHandler()
        self.file_handler = logging.FileHandler(log_file)
        error_handler = logging.FileHandler(error_file)

        for handler in [self.typing_console_handler, self.console_handler]:
            handler.setFormatter(console_formatter)

        error_handler.setFormatter(AutoGptFormatter(
            '%(asctime)s %(levelname)s %(module)s:%(lineno)d %(title)s %(message_no_color)s'
        ))

        self.typing_logger = self._create_logger('TYPER', [self.typing_console_handler, self.file_handler, error_handler])
        self.logger = self._create_logger('LOGGER', [self.console_handler, self.file_handler, error_handler])

        self._setup_log_rotation(log_file)

    def _create_logger(self, name, handlers):
        logger = logging.getLogger(name)
        for handler in handlers:
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def _setup_log_rotation(self, log_file, max_size=5*1024*1024, backup_count=5):
        if os.path.getsize(log_file) > max_size:
            for i in range(backup_count - 1, 0, -1):
                older_log = f"{log_file}.{i}"
                newer_log = f"{log_file}.{i + 1}"
                if os.path.exists(older_log):
                    os.rename(older_log, newer_log)
            os.rename(log_file, f"{log_file}.1")
            open(log_file, 'w').close()  # Clear the current log file

    def typewriter_log(self, title='', title_color='', content='', speak_text=False, level=logging.INFO):
        if speak_text and cfg.system_settings['speak_mode']:
            say_text(f"{title}. {content}")
        self.typing_logger.log(level, " ".join(content) if isinstance(content, list) else content, extra={'title': title, 'color': title_color})

    def debug(self, message, title='', title_color=''):
        self._log(title, title_color, message, logging.DEBUG)

    def warn(self, message, title='', title_color=''):
        self._log(title, title_color, message, logging.WARN)

    def error(self, title, message=''):
        self._log(title, '', message, logging.ERROR)

    def _log(self, title='', title_color='', message='', level=logging.INFO):
        self.logger.log(level, " ".join(message) if isinstance(message, list) else message, extra={'title': title, 'color': title_color})

    def set_level(self, level):
        self.logger.setLevel(level)
        self.typing_logger.setLevel(level)

    def double_check(self, additional_text=None):
        additional_text = additional_text or "Check setup/config: https://github.com/Torantulino/Auto-GPT#readme"
        self.typewriter_log("DOUBLE CHECK CONFIG", "", additional_text)

def remove_color_codes(s):
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)

def say_text(text, voice_index=0):
    try:
        speaker.Speak(text)
        return True
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return False

def read_python_exe_path():
    try:
        with open(os.path.join("data", "persistence_batch.txt"), "r") as f:
            for line in f:
                if line.startswith("python_exe="):
                    return line.split("=")[1].strip()
    except FileNotFoundError:
        return None

logger = Logger()