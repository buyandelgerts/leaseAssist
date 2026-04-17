import os
import httpx
from dotenv import load_dotenv

load_dotenv()

RENTCAST_API_KEY = os.getenv("RENTCAST_API_KEY")
RENTCAST_URL = "https://api.rentcast.io/v1/listings/rental/long-term"


async def fetch_rentcast_listings(city: str, state: str, limit: int = 20) -> list[dict]:
    if not RENTCAST_API_KEY:
        raise ValueError("RENTCAST_API_KEY is missing in .env")

    headers = {
        "X-Api-Key": RENTCAST_API_KEY,
        "Accept": "application/json",
    }

    params = {
        "city": city,
        "state": state,
        "limit": limit,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(RENTCAST_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "data" in data and isinstance(data["data"], list):
        return data["data"]

    return []