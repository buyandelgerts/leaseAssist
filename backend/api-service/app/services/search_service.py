from sqlalchemy.orm import Session
from sqlalchemy import text
from .embedding_service import get_embedding


def search_listings(
    db: Session,
    query: str,
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
    limit: int = 5
):
    query_embedding = get_embedding(query)

    sql = """
        SELECT
            rentcast_id,
            formatted_address,
            city,
            state,
            price,
            bedrooms,
            bathrooms,
            square_footage,
            content,
            1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM rental_listings
        WHERE 1=1
    """

    params = {
        "embedding": str(query_embedding),
        "limit": limit
    }

    if city:
        sql += " AND city = :city"
        params["city"] = city

    if state:
        sql += " AND state = :state"
        params["state"] = state

    if max_price is not None:
        sql += " AND price <= :max_price"
        params["max_price"] = max_price

    if min_bedrooms is not None:
        sql += " AND bedrooms >= :min_bedrooms"
        params["min_bedrooms"] = min_bedrooms

    sql += """
        ORDER BY embedding <=> CAST(:embedding AS vector)
        LIMIT :limit
    """

    result = db.execute(text(sql), params)
    rows = result.fetchall()

    formatted_results = []
    for row in rows:
        formatted_results.append({
            "rentcast_id": row.rentcast_id,
            "formatted_address": row.formatted_address,
            "city": row.city,
            "state": row.state,
            "price": row.price,
            "bedrooms": row.bedrooms,
            "bathrooms": row.bathrooms,
            "square_footage": row.square_footage,
            "content": row.content,
            "similarity": float(row.similarity) if row.similarity is not None else 0.0
        })

    return formatted_results