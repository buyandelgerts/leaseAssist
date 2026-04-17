from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import RentalListing


def semantic_search(
    db: Session,
    query_embedding: list[float],
    city: str | None = None,
    state: str | None = None,
    max_price: int | None = None,
    min_bedrooms: float | None = None,
    property_type: str | None = None,
    limit: int = 10,
):
    similarity_expr = (1 - RentalListing.embedding.cosine_distance(query_embedding)).label("similarity")

    stmt = (
        select(RentalListing, similarity_expr)
        .where(RentalListing.embedding.is_not(None))
    )

    if city:
        stmt = stmt.where(RentalListing.city.ilike(city))
    if state:
        stmt = stmt.where(RentalListing.state.ilike(state))
    if max_price is not None:
        stmt = stmt.where(RentalListing.price <= max_price)
    if min_bedrooms is not None:
        stmt = stmt.where(RentalListing.bedrooms >= min_bedrooms)
    if property_type:
        stmt = stmt.where(RentalListing.property_type.ilike(property_type))

    stmt = stmt.order_by(RentalListing.embedding.cosine_distance(query_embedding)).limit(limit)

    rows = db.execute(stmt).all()

    results = []
    for listing, similarity in rows:
        results.append(
            {
                "id": listing.id,
                "external_id": listing.external_id,
                "formatted_address": listing.formatted_address,
                "city": listing.city,
                "state": listing.state,
                "zip_code": listing.zip_code,
                "latitude": listing.latitude,
                "longitude": listing.longitude,
                "property_type": listing.property_type,
                "bedrooms": listing.bedrooms,
                "bathrooms": listing.bathrooms,
                "square_footage": listing.square_footage,
                "price": listing.price,
                "status": listing.status,
                "listing_url": listing.listing_url,
                "image_url": listing.image_url,
                "description": listing.description,
                "similarity": float(similarity) if similarity is not None else None,
            }
        )

    return results