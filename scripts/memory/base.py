import abc
from config import AbstractSingleton, Config
from llama_cpp import Llama

cfg = Config()

def get_embedding(text):
    text = text.replace("\n", " ")
    model = Llama(model_path=cfg.smart_llm_model)
    embedding = model.embed(text)
    return embedding

class MemoryProviderSingleton(AbstractSingleton):
    @abc.abstractmethod
    def add(self, data):
        pass

    @abc.abstractmethod
    def get(self, data):
        pass

    @abc.abstractmethod
    def clear(self):
        pass

    @abc.abstractmethod
    def get_relevant(self, data, num_relevant=5):
        pass

    @abc.abstractmethod
    def get_stats(self):
        pass