import requests
from utils.config import CRICBUZZ_API_KEY, CRICBUZZ_API_HOST

BASE_URL = f"https://{CRICBUZZ_API_HOST}"

HEADERS = {
    "x-rapidapi-host": CRICBUZZ_API_HOST,
    "x-rapidapi-key": CRICBUZZ_API_KEY
}

def _get(endpoint: str, params: dict = None) -> dict:
    """Internal helper: makes a GET request and returns parsed JSON."""
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def get_recent_matches() -> dict:
    return _get("/matches/v1/recent")

def get_live_matches() -> dict:
    return _get("/matches/v1/live")

def get_upcoming_matches() -> dict:
    return _get("/matches/v1/upcoming")

def get_match_scorecard(match_id: int) -> dict:
    return _get(f"/mcenter/v1/{match_id}/hscard")

def get_match_info(match_id: int) -> dict:
    return _get(f"/mcenter/v1/{match_id}")