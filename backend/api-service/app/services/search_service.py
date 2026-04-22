from sqlalchemy.orm import Session
from sqlalchemy import text
from .embedding_service import get_embedding


def search_listings(
    db: Session,
    query: str,
    city: str | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    property_type: str | None = None,
    min_bedrooms: float | None = None,
    min_bathrooms: float | None = None,
    limit: int = 5
):
    query_embedding = get_embedding(query)
    content_query = query.strip()

    sql = """
        SELECT
            rentcast_id,
            formatted_address,
            city,
            state,
            zip_code,
            property_type,
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

    if content_query:
        params["content_query"] = f"%{content_query}%"
        sql += " AND content ILIKE :content_query"

    if city:
        sql += " AND city = :city"
        params["city"] = city

    if state:
        sql += " AND state = :state"
        params["state"] = state

    if zip_code is not None:
        sql += " AND zip_code = :zip_code"
        params["zip_code"] = zip_code

    if property_type is not None:
        sql += " AND property_type = :property_type"
        params["property_type"] = property_type

    if min_bedrooms is not None:
        sql += " AND bedrooms >= :min_bedrooms"
        params["min_bedrooms"] = min_bedrooms

    if min_bathrooms is not None:
        sql += " AND bathrooms >= :min_bathrooms"
        params["min_bathrooms"] = min_bathrooms

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
            "zip_code": row.zip_code,
            "price": row.price,
            "property_type": row.property_type,
            "bedrooms": row.bedrooms,
            "bathrooms": row.bathrooms,
            "square_footage": row.square_footage,
            "content": row.content,
            "similarity": float(row.similarity) if row.similarity is not None else 0.0
        })
    return formatted_results