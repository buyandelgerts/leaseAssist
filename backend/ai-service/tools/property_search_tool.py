# tools/property_search_tool.py
from crewai.tools import tool
from typing import Optional

# In a real project this would query a database or external API.
# For now we use a rich mock dataset.
PROPERTY_DB = [
    {
        "id": "P001", "city": "Austin", "state": "TX", "address": "123 Oak Lane",
        "beds": 2, "baths": 1, "rent": 1400, "sqft": 850,
        "amenities": ["parking", "laundry", "AC"],
        "available": True, "pet_friendly": True, "lease_term": 12
    },
    {
        "id": "P002", "city": "Austin", "state": "TX", "address": "456 Maple Ave",
        "beds": 3, "baths": 2, "rent": 1900, "sqft": 1200,
        "amenities": ["parking", "gym", "pool", "AC"],
        "available": True, "pet_friendly": False, "lease_term": 12
    },
    {
        "id": "P003", "city": "Austin", "state": "TX", "address": "789 Pine St",
        "beds": 1, "baths": 1, "rent": 950, "sqft": 600,
        "amenities": ["AC", "laundry"],
        "available": True, "pet_friendly": True, "lease_term": 6
    },
    {
        "id": "P004", "city": "Dallas", "state": "TX", "address": "10 Elm Blvd",
        "beds": 2, "baths": 2, "rent": 1600, "sqft": 1000,
        "amenities": ["parking", "gym", "AC"],
        "available": True, "pet_friendly": True, "lease_term": 12
    },
    {
        "id": "P005", "city": "Los Angeles", "state": "CA", "address": "200 Sunset Dr",
        "beds": 1, "baths": 1, "rent": 2200, "sqft": 650,
        "amenities": ["AC", "rooftop"],
        "available": True, "pet_friendly": False, "lease_term": 12
    },
    {
        "id": "P006", "city": "New York", "state": "NY", "address": "55 5th Ave",
        "beds": 2, "baths": 1, "rent": 3500, "sqft": 700,
        "amenities": ["doorman", "gym"],
        "available": True, "pet_friendly": False, "lease_term": 24
    },
]

@tool("PropertySearchTool")
def property_search_tool(
    city: str,
    max_budget: float,
    min_beds: int = 1,
    pet_friendly: Optional[bool] = None
) -> str:
    """
    Searches available properties by city, budget, and bedroom count.
    Returns top 3 ranked matches with full details.

    Args:
        city: Target city name (e.g. 'Austin', 'Los Angeles')
        max_budget: Maximum monthly rent in USD
        min_beds: Minimum number of bedrooms needed
        pet_friendly: True if tenant has pets, False/None if not required
    """
    results = []
    for p in PROPERTY_DB:
        if not p["available"]:
            continue
        if p["city"].lower() != city.lower():
            continue
        if p["rent"] > max_budget:
            continue
        if p["beds"] < min_beds:
            continue
        if pet_friendly and not p["pet_friendly"]:
            continue

        # Compute match score (0–100)
        budget_score = max(0, 40 * (1 - (p["rent"] / max_budget)))
        bed_score = 30 if p["beds"] == min_beds else 20
        amenity_score = min(30, len(p["amenities"]) * 6)
        total_score = budget_score + bed_score + amenity_score
        results.append({**p, "match_score": round(total_score)})

    if not results:
        return f"No available properties found in {city} within ${max_budget}/month with {min_beds}+ beds."

    results.sort(key=lambda x: x["match_score"], reverse=True)
    top3 = results[:3]

    output = f"=== TOP {len(top3)} PROPERTIES IN {city.upper()} ===\n"
    for i, p in enumerate(top3, 1):
        amenities_str = ", ".join(p["amenities"])
        output += f"""
Match #{i} — Score: {p['match_score']}/100
  Address    : {p['address']}, {p['city']}, {p['state']}
  Rent       : ${p['rent']:,}/month
  Size       : {p['beds']} bed / {p['baths']} bath — {p['sqft']} sqft
  Amenities  : {amenities_str}
  Pet-friendly: {'Yes' if p['pet_friendly'] else 'No'}
  Lease term : {p['lease_term']} months
  Property ID: {p['id']}
"""
    return output