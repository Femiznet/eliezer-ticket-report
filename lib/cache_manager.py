import json
from pathlib import Path
import utils

class CacheManager:
    _cachePath = Path("cache")
    _cachePath.mkdir(exist_ok=True)

    @classmethod
    def save(cls, data: dict, file:str):
        filepath = cls._cachePath / file
        file_suffix = filepath.suffix

        try:
            if file_suffix.lower() != ".json":
                utils.logError(f"Unsupported extension: {file_suffix}. Only .json allowed.")
                return
            
            # Ensure folder (cache/) exists before writing
            filepath.mkdir(parents=True, exist_ok=True)
            
            with filepath.open("w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            utils.logError("Saving cache failed", e)

    @classmethod
    def load(cls, file:str) -> list:
        filepath = cls._cachePath / file
        try:
            with filepath.open() as f:
                return json.load(f)
        except Exception as e:
            utils.log_error("Loading cache failed", e)

        return []

if __name__ == "__main__":
    CacheManager().save({"femi":"boy"})