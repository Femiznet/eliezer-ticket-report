import requests
from lib.utils import log_error
from lib import config

class ZohoQueryBuilder:
    @staticmethod
    def build_extraction_params(status: str, date_range: str, offset: int = 0) -> dict:
        status_lower = status.lower()
        time_key = "createdTimeRange" if status_lower == "open" else "modifiedTimeRange"
        return {
            "from": offset,
            "limit": 100,
            "status": status_lower,
            time_key: date_range
        }

    @staticmethod
    def build_extraction_headers(auth_token: str) -> dict:
        if not auth_token or not auth_token.strip():
            raise ValueError("Missing or empty auth token")
        return {
            "Authorization": f"Zoho-oauthtoken {auth_token.strip()}",
            "orgId": str(config.ORG_ID)
        }

    @staticmethod
    def build_refresh_payload(ref_token: str, client_id: str, client_secret: str) -> dict:
        if not all([ref_token, client_id, client_secret]):
            raise ValueError("Auth credentials missing.")
        return {
            "refresh_token": ref_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token"
        }

class ZohoAPI:
    def __init__(self, timeout=10):
        self.session = requests.Session()
        self.timeout = timeout
    
    def _handle_request(self, method, url, **kwargs):
        """Unified internal function to share error handling and request logic."""
        kwargs.setdefault("timeout", self.timeout)
        try:
            response = self.session.request(method, url, **kwargs)
            if response.status_code == 401:
                return 401
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            log_error("Invalid JSON response from API", e)
            return None
        except requests.exceptions.Timeout as e:
            log_error(f"Request timeout at {url} (timeout={self.timeout}s)", e)
            raise
        except requests.exceptions.ConnectionError as e:
            log_error(f"Connection error at {url}", e)
            raise
        except requests.exceptions.RequestException as e:
            log_error(f"Request failed at {url}", e)
            raise

    def request_data(self, url, params, headers):
        data = self._handle_request("GET", url, params=params, headers=headers)
        return data.get("data") if isinstance(data, dict) else data

    def refresh_token(self, url, payload):
        data = self._handle_request("POST", url, data=payload)
        
        if not data or not isinstance(data, dict):
            raise ValueError("Failed to refresh token: Invalid response structure.")

        return data.get("access_token")

    def close(self):
        self.session.close()


