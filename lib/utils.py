import logging
from lib import config
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

def get_auth_token(file_path: str) -> str:
    path = Path(file_path)
    path.touch(exist_ok=True)

    token = path.read_text().strip()
    
    return token

def save_token(token:str, file_path:str):
    if not token:
        log_error("Saving new token failed")
        return
    with open(file_path, "w") as file:
        file.write(token.strip())
