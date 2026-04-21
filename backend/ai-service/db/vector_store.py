import os
from typing import Any, Optional
from openai import OpenAI
from pgvector.psycopg2 import register_vector
from .connection import get_connection

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
EMBED_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-3-small")


def embed_text(text: str) -> list[float]:
    """Convert a text string into a vector embedding."""
    response = client.embeddings.create(input=text, model=EMBED_MODEL)
    return response.data[0].embedding


def similarity_search(
    query: Optional[str] = None,
    city: str = "",
    state: str = "",
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    cleaned_query = (query or "").strip()
    cleaned_city = city.strip()
    cleaned_state = state.strip()

    if not cleaned_city or not cleaned_state:
        raise ValueError("Both city and state are required for similarity_search.")

    where_clauses: list[str] = ["LOWER(city) = LOWER(%s)", "UPPER(state) = UPPER(%s)"]
    where_params: list[Any] = [cleaned_city, cleaned_state]

    if cleaned_query:
        query_vector = embed_text(cleaned_query)
        sql = """
            SELECT
                id,
                formatted_address,
                city,
                state,
                zip_code,
                property_type,
                price,
                bedrooms,
                bathrooms,
                square_footage,
                listing_type,
                content,
                1.0 / (1.0 + (embedding <=> %s::vector)) AS similarity_score
            FROM rental_listings
        """
        params: list[Any] = [query_vector, *where_params, query_vector]
        sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY embedding <=> %s::vector"
        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)
        sql += ";"
    else:
        sql = """
            SELECT
                id,
                formatted_address,
                city,
                state,
                zip_code,
                property_type,
                price,
                bedrooms,
                bathrooms,
                square_footage,
                listing_type,
                content,
                NULL::float AS similarity_score
            FROM rental_listings
        """
        params = [*where_params]
        sql += " WHERE " + " AND ".join(where_clauses)
        sql += " ORDER BY id DESC"
        if limit is not None:
            sql += " LIMIT %s"
            params.append(limit)
        sql += ";"

    results = []
    with get_connection() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            for row in cur.fetchall():
                results.append({
                    "id": row[0],
                    "formatted_address": row[1],
                    "city": row[2],
                    "state": row[3],
                    "zip_code": row[4],
                    "property_type": row[5],
                    "price": row[6],
                    "bedrooms": row[7],
                    "bathrooms": row[8],
                    "square_footage": row[9],
                    "listing_type": row[10],
                    "content": row[11],
                    "similarity_score": float(row[12]) if row[12] is not None else None,
                })

    return results