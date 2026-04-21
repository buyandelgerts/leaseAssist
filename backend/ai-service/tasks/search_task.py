from typing import Optional
from crewai import Task
from crewai import Agent

def create_search_task(agent: Agent, query: Optional[str] = None, city: str = "", state: str = "") -> Task:
    query_text = query or ""
    return Task(
        description=(
            f"Search the vector database and return results based on the provided inputs and query.\n\n"
            f"  QUERY: {query_text}\n"
            f"  CITY: {city}\n"
            f"  STATE: {state}\n\n"
            "Steps:\n"
            "1. Use the vector_search tool with the provided query, city, and state values.\n"
            "2. Detect numeric budget intent from the query (for example: 'under 600', '<= 600', 'max 600', 'up to 600 per month').\n"
            "3. If a budget is detected, treat it as monthly price and filter out any listing whose price is greater than that max.\n"
            "4. Match the query semantically against each document's content field to find similar listings.\n"
            "5. Enforce city and state as exact filters when they are provided in the inputs.\n"
            "6. Return only results that satisfy all detected filters (city/state/budget) and are relevant to the query-content similarity.\n"
            "7. Sort remaining results by similarity_score descending.\n"
            "8. Summarize each result with its ID, city, state, zip_code, property_type, price, bedrooms, bathrooms, square_footage, listing_type, content, and similarity score.\n"
            "9. Return all results in structured JSON format."
        ),
        expected_output=(
            "A JSON object containing: 'query', 'city', 'state', 'max_price' (null if not detected), 'total_found', and a 'results' array "
            "where each item has 'id', 'city', 'state', 'zip_code', 'property_type', 'price', 'bedrooms', 'bathrooms', 'square_footage', 'listing_type', 'content', and 'similarity_score'."
        ),
        agent=agent,
    )