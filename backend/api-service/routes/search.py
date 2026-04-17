from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas import SearchRequest, SearchResponse
from services.embedding_service import get_embedding
from services.search_service import semantic_search

router = APIRouter(prefix="/api/search", tags=["Search"])


@router.post("/", response_model=SearchResponse)
def search(payload: SearchRequest, db: Session = Depends(get_db)):
    query_embedding = get_embedding(payload.query)

    results = semantic_search(
        db=db,
        query_embedding=query_embedding,
        city=payload.city,
        state=payload.state,
        max_price=payload.max_price,
        min_bedrooms=payload.min_bedrooms,
        property_type=payload.property_type,
        limit=payload.limit,
    )

    return SearchResponse(results=results)