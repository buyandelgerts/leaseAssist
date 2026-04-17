import os
import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def search_listings_tool(
    query: str,
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
    property_type: str | None = None,
    limit: int = 5,
):
    payload = {
        "query": query,
        "city": city,
        "state": state,
        "max_price": max_price,
        "min_bedrooms": min_bedrooms,
        "property_type": property_type,
        "limit": limit,
    }

    response = requests.post(f"{BACKEND_URL}/api/search/", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = search_listings_tool(
        query="quiet 2 bedroom apartment near downtown with parking",
        city="Chicago",
        state="IL",
        max_price=2500,
        min_bedrooms=2,
        limit=3,
    )
    print(result)