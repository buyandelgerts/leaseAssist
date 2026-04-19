import os

import httpx
from crewai.tools import tool

API_SERVICE_URL = os.getenv("API_SERVICE_URL", "http://localhost:8001")


@tool("ListingSearchTool")
def listing_search_tool(
    query: str,
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
) -> str:
    """
    Search real rental listings from the database.
    Use this when a user asks about apartments, rentals, or properties.

    Args:
        query: Natural language description of what you're looking for
        city: City to search in (e.g. 'Austin')
        state: State abbreviation (e.g. 'TX')
        max_price: Maximum monthly rent in USD
        min_bedrooms: Minimum number of bedrooms

    Returns a formatted list of matching listings with address, price, beds, baths, and sqft.
    """
    payload: dict = {"query": query, "limit": 5}
    console.log(city, state, max_price, min_bedrooms)
    if city:
        payload["city"] = city
    if state:
        payload["state"] = state
    if max_price is not None:
        payload["max_price"] = max_price
    if min_bedrooms is not None:
        payload["min_bedrooms"] = min_bedrooms

    try:
        response = httpx.post(
            f"{API_SERVICE_URL}/search", json=payload, timeout=10.0
        )
        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return "No listings found in the database matching your criteria."

        lines = [
            f"• {r.get('formatted_address', 'N/A')} — "
            f"${r.get('price', '?')}/mo, "
            f"{r.get('bedrooms', '?')}bd/{r.get('bathrooms', '?')}ba, "
            f"{r.get('sqft', 'N/A')} sqft"
            for r in results
        ]
        return "\n".join(lines)
    except httpx.ConnectError:
        return "Listing database is currently unavailable. Please try again later."
    except Exception as e:
        return f"Could not retrieve listings: {str(e)}"
