import os
import requests
from dotenv import load_dotenv

load_dotenv()

RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
RENTCAST_BASE_URL = os.getenv("RENTCAST_BASE_URL")


def fetch_rentcast_listings(city: str, state: str, status: str = "Active", limit: int = 5) -> list:
    headers = {
        "X-Api-Key": RENTCAST_API_KEY,
        "Accept": "application/json"
    }

    params = {
        "city": city,
        "state": state,
        "status": status,
        "limit": limit
    }

    response = requests.get(RENTCAST_BASE_URL, headers=headers, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, list):
        return data

    return []