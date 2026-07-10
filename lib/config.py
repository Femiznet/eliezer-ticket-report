from dotenv import load_dotenv
import os

def required(key: str) -> str:
    value = os.getenv(key)
    if not value or not value.strip():
        raise EnvironmentError(f"Missing required environment variable: [{key}]")
    return value.strip()

load_dotenv()

# EXTRACTED DATA CONFIG
DEFAULT_ASSIGNEE = required("DEFAULT_ASSIGNEE")
OWNERS = required("OWNERS")

# ZOHO CONFIG
ORG_ID = required("ORG_ID")
CLIENT_ID = required("CLIENT_ID")
CLIENT_SECRET = required("CLIENT_SECRET")
REFRESH_TOKEN = required("REFRESH_TOKEN")
ZOHO_DESK_URL = required("ZOHO_DESK_URL")
ZOHO_REFRESH_URL = required("REFRESH_URL")

# REFRESH TOKEN CONFIG
TOKEN_FILE = "token.env"
TOKEN_VAR = "AUTH_TOKEN"

# FILE CONFIG
CACHE_FILE = "raw.json"
SAVE_TO_PATH = "tickets"
ERROR_LOG_PATH = "log/error.log"

# DATE
DEFAULT_DATE = "1 JAN 2025"