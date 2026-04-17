from sqlalchemy.orm import Session
from ..models import RentalListing
from .embedding_service import get_embedding


def listing_to_content(listing: dict) -> str:
    address = listing.get("formattedAddress", "")
    city = listing.get("city", "")
    state = listing.get("state", "")
    property_type = listing.get("propertyType", "")
    price = listing.get("price", "")
    bedrooms = listing.get("bedrooms", "")
    bathrooms = listing.get("bathrooms", "")
    square_footage = listing.get("squareFootage", "")
    status = listing.get("status", "")

    features = listing.get("features", {}) or {}
    feature_parts = []

    if isinstance(features, dict):
        for key, value in features.items():
            if value not in [None, "", False]:
                feature_parts.append(f"{key}: {value}")

    features_text = ", ".join(feature_parts)

    content = (
        f"Rental listing at {address}, {city}, {state}. "
        f"Property type: {property_type}. "
        f"Price: ${price} per month. "
        f"Bedrooms: {bedrooms}. "
        f"Bathrooms: {bathrooms}. "
        f"Square footage: {square_footage}. "
        f"Status: {status}. "
        f"Features: {features_text}."
    )

    return content.strip()


def upsert_listing(db: Session, listing: dict) -> RentalListing:
    rentcast_id = str(listing.get("id"))
    content = listing_to_content(listing)
    embedding = get_embedding(content)

    existing = db.query(RentalListing).filter(RentalListing.rentcast_id == rentcast_id).first()

    if existing:
        existing.formatted_address = listing.get("formattedAddress")
        existing.city = listing.get("city")
        existing.state = listing.get("state")
        existing.zip_code = listing.get("zipCode")
        existing.latitude = listing.get("latitude")
        existing.longitude = listing.get("longitude")
        existing.property_type = listing.get("propertyType")
        existing.bedrooms = listing.get("bedrooms")
        existing.bathrooms = listing.get("bathrooms")
        existing.square_footage = listing.get("squareFootage")
        existing.price = listing.get("price")
        existing.status = listing.get("status")
        existing.listing_type = listing.get("listingType")
        existing.features = listing.get("features", {})
        existing.raw_json = listing
        existing.content = content
        existing.embedding = embedding

        db.commit()
        db.refresh(existing)
        return existing

    new_listing = RentalListing(
        rentcast_id=rentcast_id,
        formatted_address=listing.get("formattedAddress"),
        city=listing.get("city"),
        state=listing.get("state"),
        zip_code=listing.get("zipCode"),
        latitude=listing.get("latitude"),
        longitude=listing.get("longitude"),
        property_type=listing.get("propertyType"),
        bedrooms=listing.get("bedrooms"),
        bathrooms=listing.get("bathrooms"),
        square_footage=listing.get("squareFootage"),
        price=listing.get("price"),
        status=listing.get("status"),
        listing_type=listing.get("listingType"),
        features=listing.get("features", {}),
        raw_json=listing,
        content=content,
        embedding=embedding
    )

    db.add(new_listing)
    db.commit()
    db.refresh(new_listing)
    return new_listing