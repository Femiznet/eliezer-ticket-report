import logging
import config
from pathlib import Path

# Set up the base configuration
log_file = Path(config.ERROR_LOG_PATH)
log_dir = log_file.parent

log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=config.ERROR_LOG_PATH
)

def log_error(message, error=None):
    """Refined logging function to handle both messages and tracebacks."""
    logger = logging.getLogger(__name__)
    if error:
        # captures the full stack trace
        logger.exception(f"{message}: {error}")
    else:
        logger.error(message)

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
