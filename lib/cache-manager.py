import json
import logging
from pathlib import Path
from lib import config

class CacheManager:
    def __init__(self, default_file: str = config.CACHE_FILE):
        self.default_file = Path(default_file)
        self.logger = logging.getLogger(__name__)

    def delete(self, file_path: str):
        Path(file_path).unlink(missing_ok=True)

    def save(self, data: dict, file_path: str | None = None):
        target = Path(file_path or self.default_file)
        try:
            if target.suffix.lower() != ".json":
                raise ValueError(f"Unsupported extension: {target.suffix}. Only .json allowed.")
            
            # Ensure folder (cache/) exists before writing
            target.parent.mkdir(parents=True, exist_ok=True)
            
            with target.open("w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Caching failed for {target}: {e}")
            raise

    def load(self, file_path: str | None = None) -> dict:
        path = Path(file_path or self.default_file)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Expected file, found directory: {path}")
        if path.suffix.lower() != ".json":
            raise TypeError(f"Invalid file type: {path.suffix}. Must be .json")
        
        with path.open() as f:
            return json.load(f)