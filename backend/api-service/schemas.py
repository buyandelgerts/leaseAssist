from typing import Any
from pydantic import BaseModel, Field, ConfigDict


class SyncListingsRequest(BaseModel):
    city: str
    state: str
    limit: int = 20


class ListingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    external_id: str | None = None
    formatted_address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None
    bedrooms: float | None = None
    bathrooms: float | None = None
    square_footage: int | None = None
    price: int | None = None
    status: str | None = None
    listing_url: str | None = None
    image_url: str | None = None
    description: str | None = None
    searchable_text: str | None = None


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    city: str | None = None
    state: str | None = None
    max_price: int | None = None
    min_bedrooms: float | None = None
    property_type: str | None = None
    limit: int = 10


class SearchResultItem(BaseModel):
    id: int
    external_id: str | None = None
    formatted_address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None
    bedrooms: float | None = None
    bathrooms: float | None = None
    square_footage: int | None = None
    price: int | None = None
    status: str | None = None
    listing_url: str | None = None
    image_url: str | None = None
    description: str | None = None
    similarity: float | None = None


class SearchResponse(BaseModel):
    results: list[SearchResultItem]


class MessageResponse(BaseModel):
    message: str
    count: int | None = None


class RawListingUpsert(BaseModel):
    external_id: str | None = None
    formatted_address: str | None = None
    city: str | None = None
    state: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    property_type: str | None = None
    bedrooms: float | None = None
    bathrooms: float | None = None
    square_footage: int | None = None
    lot_size: int | None = None
    year_built: int | None = None
    price: int | None = None
    status: str | None = None
    listing_url: str | None = None
    image_url: str | None = None
    description: str | None = None
    raw_json: dict[str, Any]
    searchable_text: str
    embedding: list[float] | None = None