from pydantic import BaseModel, Field
from typing import Any, Literal, Optional

class SearchResult(BaseModel):
    id: int
    content: str
    metadata: dict[str, Any] = {}
    similarity_score: float


class SearchOutput(BaseModel):
    query: str
    results: list[SearchResult]
    total_found: int


class EligibilityInput(BaseModel):
    applicant_data: dict[str, Any] = Field(
        description="Key-value pairs describing the applicant"
    )
    search_results: list[SearchResult] = Field(
        description="Relevant documents from the vector search"
    )


class EligibilityOutput(BaseModel):
    is_eligible: bool
    confidence_score: float = Field(ge=0.0, le=1.0)
    reasons: list[str]
    applied_rules: list[str]
    recommendation: str


class RouteButton(BaseModel):
    label: str
    route: str


class ChatbotResponse(BaseModel):
    type: Literal["text", "apartments", "route"]
    message: str
    apartments: Optional[list[dict]] = None
    buttons: Optional[list[RouteButton]] = None