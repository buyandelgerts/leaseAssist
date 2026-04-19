import os
import json
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from openai import OpenAI

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

mcp = FastMCP("LeaseAssist Listings")


def _get_embedding(text_input: str) -> list:
    resp = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text_input
    )
    return resp.data[0].embedding


@mcp.tool()
def search_listings(
    query: str,
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
    limit: int = 5
) -> str:
    """
    Search rental listings using semantic vector search with optional filters.

    Args:
        query: Natural language description (e.g. '2-bed apartment near downtown')
        city: Filter by city name (e.g. 'Austin')
        state: Filter by state abbreviation (e.g. 'TX')
        max_price: Maximum monthly rent in USD
        min_bedrooms: Minimum number of bedrooms
        limit: Max results to return (default 5)
    """
    embedding = _get_embedding(query)

    sql = """
        SELECT rentcast_id, formatted_address, city, state, price,
               bedrooms, bathrooms, square_footage, content,
               1 - (embedding <=> CAST(:embedding AS vector)) AS similarity
        FROM rental_listings WHERE 1=1
    """
    params: dict = {"embedding": str(embedding), "limit": limit}

    if city:
        sql += " AND LOWER(city) = LOWER(:city)"
        params["city"] = city
    if state:
        sql += " AND UPPER(state) = UPPER(:state)"
        params["state"] = state
    if max_price is not None:
        sql += " AND price <= :max_price"
        params["max_price"] = max_price
    if min_bedrooms is not None:
        sql += " AND bedrooms >= :min_bedrooms"
        params["min_bedrooms"] = min_bedrooms

    sql += " ORDER BY embedding <=> CAST(:embedding AS vector) LIMIT :limit"

    db = SessionLocal()
    try:
        rows = db.execute(text(sql), params).fetchall()
        results = [
            {
                "address": r.formatted_address,
                "city": r.city,
                "state": r.state,
                "price": r.price,
                "bedrooms": r.bedrooms,
                "bathrooms": r.bathrooms,
                "sqft": r.square_footage,
                "similarity": round(float(r.similarity or 0), 3),
            }
            for r in rows
        ]
        if not results:
            return "No listings found matching your criteria."
        return json.dumps(results, indent=2)
    finally:
        db.close()


@mcp.tool()
def get_listing(rentcast_id: str) -> str:
    """
    Get full details of a specific rental listing by its rentcast_id.

    Args:
        rentcast_id: The unique RentCast listing identifier
    """
    db = SessionLocal()
    try:
        row = db.execute(
            text("SELECT * FROM rental_listings WHERE rentcast_id = :id"),
            {"id": rentcast_id},
        ).fetchone()
        if not row:
            return json.dumps({"error": f"Listing '{rentcast_id}' not found"})
        return json.dumps(
            {
                "address": row.formatted_address,
                "city": row.city,
                "state": row.state,
                "price": row.price,
                "bedrooms": row.bedrooms,
                "bathrooms": row.bathrooms,
                "sqft": row.square_footage,
                "features": row.features,
                "status": row.status,
                "listing_type": row.listing_type,
            }
        )
    finally:
        db.close()


# Expose as ASGI app so uvicorn can serve it:
#   uvicorn mcp_server:app --port 8002
app = mcp.sse_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
