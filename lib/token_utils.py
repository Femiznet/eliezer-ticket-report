from pathlib import Path

def get_auth_token(file: str) -> str:
    filepath = Path(file)
    if not filepath.exists():
        filepath.touch(exist_ok=True)
        return None

    return filepath.read_text().strip()

def save_token(token:str, file:str):
    if not token:
        raise ValueError("cannot save an empty token")

    with open(file, "w") as f:
        f.write(token)
