from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import IngestRequest
from ..services.rentcast_service import fetch_rentcast_listings
from ..services.listing_service import upsert_listing

router = APIRouter(prefix="/listings", tags=["Listings"])


@router.post("/ingest")
def ingest_listings(payload: IngestRequest, db: Session = Depends(get_db)):
    try:
        listings = fetch_rentcast_listings(
            city=payload.city,
            state=payload.state,
            status=payload.status,
            limit=payload.limit
        )

        saved_items = []
        for listing in listings:
            saved = upsert_listing(db, listing)
            saved_items.append({
                "rentcast_id": saved.rentcast_id,
                "formatted_address": saved.formatted_address,
                "price": saved.price
            })

        return {
            "message": "Listings ingested successfully",
            "count": len(saved_items),
            "items": saved_items
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))