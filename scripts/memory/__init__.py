from memory.local import LocalCache
from memory.no_memory import NoMemory

# List of supported memory backends
supported_memory = ['local', 'no_memory']

def get_memory(cfg, init=False):
    memory = None
    if cfg.memory_backend == "no_memory":
        memory = NoMemory(cfg)
    else:
        memory = LocalCache(cfg)
        if init:
            memory.clear()
    return memory

def get_supported_memory_backends():
    return supported_memory

__all__ = [
    "get_memory",
    "LocalCache",
    "NoMemory"
]