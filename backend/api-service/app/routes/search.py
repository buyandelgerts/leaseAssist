from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..schemas import SearchRequest, SearchResponse
from ..services.search_service import search_listings

router = APIRouter(prefix="/search", tags=["Search"])

@router.post("", response_model=SearchResponse)
def search_apartments(payload: SearchRequest, db: Session = Depends(get_db)):
    try:
        results = search_listings(
            db=db,
            query=payload.query,
            city=payload.city,
            state=payload.state,
            max_price=payload.max_price,
            min_bedrooms=payload.min_bedrooms,
            limit=payload.limit
        )

        return {"results": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))