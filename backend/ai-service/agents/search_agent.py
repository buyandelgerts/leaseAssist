from crewai import Agent
from tools.vector_search_tool import VectorSearchTool


def create_search_agent() -> Agent:
    return Agent(
        role="Knowledge Retrieval Specialist",
        goal=(
            "Search the vector database to find the most relevant documents "
            "for any given query, and return structured, ranked results."
        ),
        backstory=(
            "You are an expert at semantic search. You understand how to formulate "
            "precise queries that retrieve the most relevant information from a "
            "PostgreSQL pgvector database. You rank results by similarity and always "
            "provide clear source attribution."
        ),
        tools=[VectorSearchTool()],
        verbose=True,
        allow_delegation=False,
        max_iter=3,
    )