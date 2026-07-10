from pathlib import Path

def get_auth_token(file: str) -> str:
    file = Path(file)
    if not file.exists():
        raise FileNotFoundError(f"{file} does not exists")
    
    token = file.read_text().strip()
    if not token:
        raise ValueError(f"File:{file} is empty")
    
    return token

def save_token(token:str, file:str):
    if not token:
        raise ValueError("cannot save an empty token")

    with open(file, "w") as f:
        f.write(token)
