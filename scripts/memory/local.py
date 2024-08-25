import dataclasses
import orjson
from typing import Any, List, Optional
import numpy as np
import os
from memory.base import MemoryProviderSingleton
from config import Config

cfg = Config()
SAVE_OPTIONS = orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_SERIALIZE_DATACLASS

def create_default_embeddings():
    return np.zeros((0, cfg.embed_dim)).astype(np.float32)

@dataclasses.dataclass
class CacheContent:
    texts: List[str] = dataclasses.field(default_factory=list)
    embeddings: np.ndarray = dataclasses.field(
        default_factory=create_default_embeddings
    )

class LocalCache(MemoryProviderSingleton):

    def __init__(self, cfg) -> None:
        self.filename = f"{cfg.memory_index}.json"
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r+b') as f:
                    file_content = f.read()
                    if not file_content.strip():
                        file_content = b'{}'
                        f.seek(0)
                        f.write(file_content)
                        f.truncate()

                    loaded = orjson.loads(file_content)
                    self.data = CacheContent(**loaded)
            except orjson.JSONDecodeError:
                print(f"Error: The file '{self.filename}' is not in JSON format.")
                self.data = CacheContent()
        else:
            print(f"Warning: The file '{self.filename}' does not exist. Local memory would not be saved to a file.")
            self.data = CacheContent()

    def add(self, text: str):
        if 'Command Error:' in text:
            return ""
        self.data.texts.append(text)

        embedding = self.get_embedding(text)

        vector = np.array(embedding).astype(np.float32)
        vector = vector[np.newaxis, :]
        self.data.embeddings = np.concatenate(
            [
                self.data.embeddings,
                vector,
            ],
            axis=0,
        )

        with open(self.filename, 'wb') as f:
            out = orjson.dumps(
                self.data,
                option=SAVE_OPTIONS
            )
            f.write(out)
        return text

    def clear(self) -> str:
        self.data = CacheContent()
        return "Memory cleared"

    def get(self, data: str) -> Optional[List[Any]]:
        return self.get_relevant(data, 1)

    def get_relevant(self, text: str, k: int) -> List[Any]:
        embedding = self.get_embedding(text)

        scores = np.dot(self.data.embeddings, embedding)

        top_k_indices = np.argsort(scores)[-k:][::-1]

        return [self.data.texts[i] for i in top_k_indices]

    def get_stats(self):
        return len(self.data.texts), self.data.embeddings.shape

    def get_embedding(self, text: str) -> List[float]:
        # Implement your local model's embedding function here
        # This is a placeholder and should be replaced with actual embedding logic
        return [0.0] * cfg.embed_dim