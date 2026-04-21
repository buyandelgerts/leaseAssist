from typing import Optional
from crewai import Task
from crewai import Agent

def create_search_task(agent: Agent, query: Optional[str] = None, city: str = "", state: str = "") -> Task:
    query_text = query or ""
    return Task(
        description=(
            f"Search the vector database for documents relevant to the following query:\n\n"
            f"  QUERY: {query_text}\n"
            f"  CITY: {city}\n"
            f"  STATE: {state}\n\n"
            "Steps:\n"
            "1. Use the vector_search tool with the provided query, city, and state.\n"
            "2. Retrieve the top 5 most similar documents.\n"
            "3. Summarize each result with its ID, content snippet, and similarity score.\n"
            "4. Return all results in structured JSON format."
        ),
        expected_output=(
            "A JSON object containing: 'query', 'city', 'state', 'total_found', and a 'results' array "
            "where each item has 'id', 'content', 'metadata', and 'similarity_score'."
        ),
        agent=agent,
    )