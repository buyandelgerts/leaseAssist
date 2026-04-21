from pydantic import BaseModel
from typing import Optional, List, Any

class IngestRequest(BaseModel):
    city: str
    state: str
    status: str = "Active"
    limit: int = 5


class ListingResponse(BaseModel):
    rentcast_id: str
    formatted_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    property_type: Optional[str] = None
    bedrooms: Optional[float] = None
    bathrooms: Optional[float] = None
    square_footage: Optional[int] = None
    price: Optional[int] = None
    status: Optional[str] = None
    listing_type: Optional[str] = None
    features: Optional[Any] = None
    content: str
    class Config:
        from_attributes = True

class SearchRequest(BaseModel):
    query: str
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    min_bedrooms: Optional[float] = None
    min_bathrooms: Optional[float] = None
    limit: int = 5


class SearchResult(BaseModel):
    rentcast_id: str
    formatted_address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    property_type: Optional[str] = None
    price: Optional[int] = None
    bedrooms: Optional[float] = None
    bathrooms: Optional[float] = None
    square_footage: Optional[int] = None
    content: str
    similarity: float


class SearchResponse(BaseModel):
    results: List[SearchResult]