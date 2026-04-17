from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from models import RentalListing
from schemas import RawListingUpsert


def build_searchable_text(listing: dict) -> str:
    parts = [
        f"Address: {listing.get('formattedAddress', '')}",
        f"City: {listing.get('city', '')}",
        f"State: {listing.get('state', '')}",
        f"Zip: {listing.get('zipCode', '')}",
        f"Property type: {listing.get('propertyType', '')}",
        f"Bedrooms: {listing.get('bedrooms', '')}",
        f"Bathrooms: {listing.get('bathrooms', '')}",
        f"Square feet: {listing.get('squareFootage', '')}",
        f"Price: {listing.get('price', '')}",
        f"Status: {listing.get('status', '')}",
        f"Description: {listing.get('description', '')}",
    ]
    return " | ".join([p for p in parts if p and p.strip() != ""])


def map_rentcast_listing(raw: dict, embedding: list[float] | None = None) -> RawListingUpsert:
    return RawListingUpsert(
        external_id=str(raw.get("id")) if raw.get("id") is not None else None,
        formatted_address=raw.get("formattedAddress"),
        city=raw.get("city"),
        state=raw.get("state"),
        zip_code=raw.get("zipCode"),
        latitude=raw.get("latitude"),
        longitude=raw.get("longitude"),
        property_type=raw.get("propertyType"),
        bedrooms=raw.get("bedrooms"),
        bathrooms=raw.get("bathrooms"),
        square_footage=raw.get("squareFootage"),
        lot_size=raw.get("lotSize"),
        year_built=raw.get("yearBuilt"),
        price=raw.get("price"),
        status=raw.get("status"),
        listing_url=raw.get("listingUrl"),
        image_url=raw.get("imageUrl"),
        description=raw.get("description"),
        raw_json=raw,
        searchable_text=build_searchable_text(raw),
        embedding=embedding,
    )


def upsert_listing(db: Session, listing: RawListingUpsert) -> None:
    stmt = insert(RentalListing).values(
        external_id=listing.external_id,
        source="rentcast",
        formatted_address=listing.formatted_address,
        city=listing.city,
        state=listing.state,
        zip_code=listing.zip_code,
        latitude=listing.latitude,
        longitude=listing.longitude,
        property_type=listing.property_type,
        bedrooms=listing.bedrooms,
        bathrooms=listing.bathrooms,
        square_footage=listing.square_footage,
        lot_size=listing.lot_size,
        year_built=listing.year_built,
        price=listing.price,
        status=listing.status,
        listing_url=listing.listing_url,
        image_url=listing.image_url,
        description=listing.description,
        raw_json=listing.raw_json,
        searchable_text=listing.searchable_text,
        embedding=listing.embedding,
    )

    stmt = stmt.on_conflict_do_update(
        index_elements=[RentalListing.external_id],
        set_={
            "formatted_address": stmt.excluded.formatted_address,
            "city": stmt.excluded.city,
            "state": stmt.excluded.state,
            "zip_code": stmt.excluded.zip_code,
            "latitude": stmt.excluded.latitude,
            "longitude": stmt.excluded.longitude,
            "property_type": stmt.excluded.property_type,
            "bedrooms": stmt.excluded.bedrooms,
            "bathrooms": stmt.excluded.bathrooms,
            "square_footage": stmt.excluded.square_footage,
            "lot_size": stmt.excluded.lot_size,
            "year_built": stmt.excluded.year_built,
            "price": stmt.excluded.price,
            "status": stmt.excluded.status,
            "listing_url": stmt.excluded.listing_url,
            "image_url": stmt.excluded.image_url,
            "description": stmt.excluded.description,
            "raw_json": stmt.excluded.raw_json,
            "searchable_text": stmt.excluded.searchable_text,
            "embedding": stmt.excluded.embedding,
        },
    )

    db.execute(stmt)


def get_listing_by_id(db: Session, listing_id: int) -> RentalListing | None:
    stmt = select(RentalListing).where(RentalListing.id == listing_id)
    return db.execute(stmt).scalar_one_or_none()


def get_listings(
    db: Session,
    city: str | None = None,
    state: str | None = None,
    limit: int = 20,
) -> list[RentalListing]:
    stmt = select(RentalListing)

    if city:
        stmt = stmt.where(RentalListing.city.ilike(city))
    if state:
        stmt = stmt.where(RentalListing.state.ilike(state))

    stmt = stmt.limit(limit)
    return list(db.execute(stmt).scalars().all())