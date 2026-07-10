import logging
from .config import ERROR_LOG_PATH
from pathlib import Path

# Set up the base configuration
log_file = Path(ERROR_LOG_PATH)
log_dir = log_file.parent

log_dir.mkdir(parents=True, exist_ok=True)

# Configure logging to include file and line information
logging.basicConfig(
    level=logging.INFO,
    # %(filename)s: File name, %(lineno)d: Line number
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    filename=ERROR_LOG_PATH
)

def log_error(message, error=None):
    """Logs a custom message with optional error context and full traceback."""
    logger = logging.getLogger(__name__)
    if error:
        # exc_info=True automatically adds the full traceback to the log
        logger.error(f"{message}: {error}", exc_info=True)
    else:
        logger.error(message)

