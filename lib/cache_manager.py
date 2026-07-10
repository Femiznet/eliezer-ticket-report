import json
from pathlib import Path
from .logging_utils import log_error

class CacheManager:
    _cachePath = Path("cache")
    _cachePath.mkdir(exist_ok=True)

    @classmethod
    def save(cls, data: dict, file:str):
        filepath = cls._cachePath / file
        file_suffix = filepath.suffix

        try:
            if file_suffix.lower() != ".json":
                log_error(f"Unsupported extension: {file_suffix}. Only .json allowed.")
                return
                        
            with filepath.open("w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            log_error("Saving cache failed", e)

    @classmethod
    def load(cls, file:str) -> list:
        filepath = cls._cachePath / file
        try:
            with filepath.open() as f:
                return json.load(f)
        except Exception as e:
            log_error("Loading cache failed", e)

        return []
