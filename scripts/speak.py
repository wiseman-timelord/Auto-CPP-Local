import win32com.client
from config import Config

cfg = Config()

speaker = win32com.client.Dispatch("SAPI.SpVoice")

def say_text(text, voice_index=0):
    """Speak text using Windows TTS"""
    try:
        speaker.Speak(text)
        return True
    except Exception as e:
        print(f"Error in text-to-speech: {str(e)}")
        return False