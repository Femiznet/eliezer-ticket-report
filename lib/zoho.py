import requests
from .logging_utils import log_error
from .token_utils import save_token, get_auth_token
from .config import (
    ZOHO_DESK_URL, ZOHO_REFRESH_URL, 
    ORG_ID, TOKEN_FILE, CACHE_FILE,
    REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET
    )
from .cache_manager import CacheManager

class ZohoAPI:
    def __init__(self, timeout=10):
        self.session = requests.Session()
        self.timeout = timeout
    
    def _handle_request(self, method, url, **kwargs) -> dict:
        """Unified internal function to share error handling and request logic."""
        kwargs.setdefault("timeout", self.timeout)
        try:
            response = self.session.request(method, url, **kwargs)
            if method == "GET" and response.status_code == 401:
                return 401
            response.raise_for_status()
            return response.json()
        except requests.exceptions.JSONDecodeError as e:
            log_error("Invalid JSON response from API", e)
            return {}
        except requests.exceptions.Timeout as e:
            log_error(f"Request timeout for {url} (timeout={self.timeout}s)", e)
            raise
        except requests.exceptions.ConnectionError as e:
            log_error(f"Connection error for {url}", e)
            raise
        except requests.exceptions.RequestException as e:
            log_error(f"Request failed for {url}", e)
            raise
        except requests.exceptions.HTTPError as e:
            log_error(f"Request failed for {url}", e)
            raise

    def request_data(self, url, params, headers) -> list:
        data = self._handle_request(method="GET", url=url, params=params, headers=headers)
        return data.get("data") if isinstance(data, dict) else data

    def refresh_token(self, url, payload) -> str:
        data = self._handle_request(method="POST", url=url, data=payload)
        
        if not data or not isinstance(data, dict):
            raise ValueError("Failed to refresh token: Invalid response structure.")

        return data.get("access_token")

    def close(self):
        self.session.close()


def _build_extraction_params(status: str, date_range: str, offset: int = 0) -> dict:
    status_lower = status.lower()
    time_key = "createdTimeRange" if status_lower == "open" else "modifiedTimeRange"
    return {
        "from": offset,
        "limit": 100,
        "status": status_lower,
        time_key: date_range
    }

def _build_extraction_headers(auth_token: str, org_id:str=ORG_ID) -> dict:
    return {
        "Authorization": f"Zoho-oauthtoken {auth_token}",
        "orgId": org_id
    }

def _build_refresh_payload(ref_token: str, client_id: str, client_secret: str) -> dict:
    if not all([ref_token, client_id, client_secret]):
        raise ValueError("Auth credentials missing.")
    return {
        "refresh_token": ref_token,
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token"
    }

def fetch_data_with_args(args):

    if not args.new: # dont make a new api request. load cache instead
        cached_data = CacheManager.load(CACHE_FILE)
        if cached_data:
            return cached_data

    params = _build_extraction_params(
        status=args.status,
        date_range=args.from_date + "," + args.to_date, # join string with a ","
    )

    headers = _build_extraction_headers(
        auth_token=get_auth_token(TOKEN_FILE),
        org_id=ORG_ID,
    )

    # initialize zoho api connection
    zoho_api = ZohoAPI()

    all_data = [] # store all data gotten from zoho

    while True:
        # request data from zoho
        data = zoho_api.request_data(
            url=ZOHO_DESK_URL, 
            params=params,
            headers=headers
        )

        if data == 401: # token expired

            # get a new token
            refresh_payload = _build_refresh_payload(
                ref_token=REFRESH_TOKEN,
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
            )

            new_token = zoho_api.refresh_token(
                url=ZOHO_REFRESH_URL,
                payload=refresh_payload,
            )

            save_token(new_token, file=TOKEN_FILE)

            # overwrite old header so it contains the new token
            headers = _build_extraction_headers(
                auth_token=new_token,
                org_id=ORG_ID,
            )

            continue

        all_data.extend(data) # add new data's incrementally to existing data

        if len(data) < params["limit"]: # stop if the data size is lesser than what we want
            break 

        params["from"] += params["limit"]

    CacheManager.save(all_data, CACHE_FILE)

    return all_data

