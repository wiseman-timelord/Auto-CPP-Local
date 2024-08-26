import yaml
import win32com.client
import logging, os, random, re, time
from config import Config

cfg = Config()
speaker = win32com.client.Dispatch("SAPI.SpVoice")

class Logger:
    def __init__(self):
        log_dir = os.path.join(os.path.dirname(__file__), '../logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "activity.log")
        error_file = os.path.join(log_dir, "error.log")

        console_formatter = AutoGptFormatter('%(title_color)s %(message)s')

        # Handlers
        self.typing_console_handler = TypingConsoleHandler()
        self.console_handler = ConsoleHandler()
        self.file_handler = logging.FileHandler(log_file)
        error_handler = logging.FileHandler(error_file)

        for handler in [self.typing_console_handler, self.console_handler]:
            handler.setFormatter(console_formatter)

        error_handler.setFormatter(AutoGptFormatter(
            '%(asctime)s %(levelname)s %(module)s:%(lineno)d %(title)s %(message_no_color)s'
        ))

        # Loggers
        self.typing_logger = self._create_logger('TYPER', [self.typing_console_handler, self.file_handler, error_handler])
        self.logger = self._create_logger('LOGGER', [self.console_handler, self.file_handler, error_handler])

    def _create_logger(self, name, handlers):
        logger = logging.getLogger(name)
        for handler in handlers:
            logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        return logger

    def typewriter_log(self, title='', title_color='', content='', speak_text=False, level=logging.INFO):
        if speak_text and cfg.speak_mode:
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

class TypingConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        min_speed, max_speed = 0.05, 0.01
        msg = self.format(record)
        for i, word in enumerate(msg.split()):
            print(word, end=" ", flush=True)
            time.sleep(random.uniform(min_speed, max_speed))
            min_speed, max_speed = min_speed * 0.95, max_speed * 0.95
        print()

class ConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        print(self.format(record))

class AutoGptFormatter(logging.Formatter):
    def format(self, record):
        record.title_color = f"{getattr(record, 'title', '')} "
        record.message_no_color = remove_color_codes(getattr(record, 'msg', ''))
        return super().format(record)

def remove_color_codes(s):
    return re.sub(r'\x1B[@-_][0-?]*[ -/]*[@-~]', '', s)

logger = Logger()

def clean_input(prompt=''):
    try:
        return input(prompt)
    except KeyboardInterrupt:
        print("Interrupted. Exiting...")
        exit(0)

def validate_yaml_file(file):
    try:
        with open(file) as f:
            yaml.load(f, Loader=yaml.FullLoader)
        return True, f"Validated `{file}`!"
    except FileNotFoundError:
        return False, f"File `{file}` not found"
    except yaml.YAMLError as e:
        return False, f"YAML error: {e}"

def say_text(text, voice_index=0):
    try:
        speaker.Speak(text)
        return True
    except Exception as e:
        print(f"TTS error: {e}")
        return False
