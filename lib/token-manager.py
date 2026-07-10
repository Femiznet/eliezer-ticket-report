from pathlib import Path
from lib.utils import log_error

class TokenManager:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get(self) -> str:
        self.file_path.touch(exist_ok=True)
        return self.file_path.read_text().strip()

    def save(self, token: str):
        if not token:
            log_error("Saving new token failed: Token is empty")
            return
        self.file_path.write_text(token.strip())

        