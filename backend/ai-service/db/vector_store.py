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
    min_similarity: float = 0.0,  # e.g. 0.3 to filter weak matches
) -> list[dict[str, Any]]:
    cleaned_query = (query or "").strip()
    cleaned_city = city.strip()
    cleaned_state = state.strip()

    if not cleaned_city or not cleaned_state:
        raise ValueError("Both city and state are required for similarity_search.")

    # Shared column list — no duplication between branches
    SELECT_COLS = """
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
        content
    """

    params: list[Any] = []

    if cleaned_query:
        query_vector = embed_text(cleaned_query)

        # Use a CTE so the vector literal appears only once in the query
        sql = f"""
            WITH ranked AS (
                SELECT
                    {SELECT_COLS},
                    -- Cosine distance (0 = identical, 2 = opposite)
                    -- Cosine similarity = 1 - cosine_distance  (range: -1 … 1)
                    1.0 - (embedding <=> %s::vector) AS similarity_score
                FROM rental_listings
                WHERE
                    LOWER(city)  = LOWER(%s)
                    AND UPPER(state) = UPPER(%s)
            )
            SELECT * FROM ranked
            WHERE similarity_score >= %s
            ORDER BY similarity_score DESC
        """
        params = [query_vector, cleaned_city, cleaned_state, min_similarity]

    else:
        sql = f"""
            SELECT
                {SELECT_COLS},
                NULL::float AS similarity_score
            FROM rental_listings
            WHERE
                LOWER(city)  = LOWER(%s)
                AND UPPER(state) = UPPER(%s)
            ORDER BY id DESC
        """
        params = [cleaned_city, cleaned_state]

    if limit is not None:
        sql += " LIMIT %s"
        params.append(limit)

    sql += ";"

    results = []
    with get_connection() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            columns = [desc[0] for desc in cur.description]  # resilient to column reorder
            for row in cur.fetchall():
                record = dict(zip(columns, row))
                if record["similarity_score"] is not None:
                    record["similarity_score"] = float(record["similarity_score"])
                results.append(record)

    return results