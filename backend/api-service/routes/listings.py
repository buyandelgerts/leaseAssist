from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import SyncListingsRequest, MessageResponse, ListingResponse
from app.services.rentcast_service import fetch_rentcast_listings
from app.services.embedding_service import get_embedding
from app.services.listing_service import (
    map_rentcast_listing,
    upsert_listing,
    get_listing_by_id,
    get_listings,
)

router = APIRouter(prefix="/api/listings", tags=["Listings"])


@router.post("/sync", response_model=MessageResponse)
async def sync_listings(payload: SyncListingsRequest, db: Session = Depends(get_db)):
    raw_listings = await fetch_rentcast_listings(
        city=payload.city,
        state=payload.state,
        limit=payload.limit,
    )

    count = 0
    for raw in raw_listings:
        mapped = map_rentcast_listing(raw)
        embedding = get_embedding(mapped.searchable_text)

        mapped = mapped.model_copy(update={"embedding": embedding})
        upsert_listing(db, mapped)
        count += 1

    db.commit()

    return MessageResponse(message="Listings synced successfully", count=count)


@router.get("/", response_model=list[ListingResponse])
def list_listings(
    city: str | None = None,
    state: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    return get_listings(db=db, city=city, state=state, limit=limit)


@router.get("/{listing_id}", response_model=ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = get_listing_by_id(db, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing