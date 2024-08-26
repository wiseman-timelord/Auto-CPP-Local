import dataclasses, orjson, os
import numpy as np
from typing import Any, List, Optional
from config import AbstractSingleton, Config

cfg = Config()
SAVE_OPTIONS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS

get_embedding = lambda txt: Llama(model_path=cfg.smart_llm_model).embed(txt.replace("\n", " "))
create_default_embeddings = lambda: np.zeros((0, cfg.embed_dim), np.float32)

@dataclasses.dataclass
class CacheContent:
    texts: List[str] = dataclasses.field(default_factory=list)
    embeddings: np.ndarray = dataclasses.field(default_factory=create_default_embeddings)

class MemoryProviderSingleton(AbstractSingleton):
    def add(self, data: str) -> str: pass
    def get(self, data: str) -> Optional[List[Any]]: pass
    def clear(self) -> str: pass
    def get_relevant(self, data: str, num_relevant: int = 5) -> List[Any]: pass
    def get_stats(self) -> Any: pass

class LocalCache(MemoryProviderSingleton):
    def __init__(self, cfg) -> None:
        self.filename = f"{cfg.memory_index}.json"
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r+b') as f:
                    content = f.read() or b'{}'
                    self.data = CacheContent(**orjson.loads(content))
            except orjson.JSONDecodeError:
                print(f"Error: {self.filename} not JSON.")
                self.data = CacheContent()
        else:
            print(f"Warning: {self.filename} missing.")
            self.data = CacheContent()

    def add(self, text: str) -> str:
        if 'Command Error:' not in text:
            self.data.texts.append(text)
            vec = np.array(get_embedding(text), np.float32)[np.newaxis, :]
            self.data.embeddings = np.concatenate([self.data.embeddings, vec], axis=0)
            with open(self.filename, 'wb') as f:
                f.write(orjson.dumps(self.data, option=SAVE_OPTIONS))
        return text

    clear = lambda self: "Memory cleared"

    def get(self, data: str) -> Optional[List[Any]]:
        return self.get_relevant(data, 1)

    def get_relevant(self, txt: str, k: int = 5) -> List[Any]:
        scores = np.dot(self.data.embeddings, get_embedding(txt))
        return [self.data.texts[i] for i in np.argsort(scores)[-k:][::-1]]

    def get_stats(self):
        return len(self.data.texts), self.data.embeddings.shape
