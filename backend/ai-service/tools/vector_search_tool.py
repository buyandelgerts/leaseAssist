from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from db.vector_store import similarity_search
import json
from typing import Optional

class VectorSearchInput(BaseModel):
    query: Optional[str] = Field(default=None, description="Optional semantic query text")
    city: str = Field(description="Target city to search in")
    state: str = Field(description="Target state to search in")
    limit: int = Field(default=10000, description="Number of results to return")


class VectorSearchTool(BaseTool):
    name: str = "vector_search"
    description: str = (
        "Search a PostgreSQL vector database (pgvector) for documents "
        "semantically similar to the provided query. Returns the most "
        "relevant documents along with their similarity scores."
    )
    args_schema: type[BaseModel] = VectorSearchInput

    def _run(self, city: str, state: str, query: Optional[str] = None, limit: int = 10000) -> str:
        query = (query or "").strip() or None
        results = similarity_search(query=query, city=city, state=state, limit=limit)

        if not results:
            return json.dumps({"message": "No results found.", "results": []})

        return json.dumps({
            "query": query,
            "city": city,
            "state": state,
            "total_found": len(results),
            "results": results,
        }, indent=2, default=str)