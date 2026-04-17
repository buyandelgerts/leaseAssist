from sqlalchemy import Column, BigInteger, Text, Integer, Float, JSON, DateTime
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from .db import Base

class RentalListing(Base):
    __tablename__ = "rental_listings"

    id = Column(BigInteger, primary_key=True, index=True)
    rentcast_id = Column(Text, unique=True, nullable=False, index=True)
    formatted_address = Column(Text)
    city = Column(Text, index=True)
    state = Column(Text, index=True)
    zip_code = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    property_type = Column(Text)
    bedrooms = Column(Float)
    bathrooms = Column(Float)
    square_footage = Column(Integer)
    price = Column(Integer, index=True)
    status = Column(Text)
    listing_type = Column(Text)
    features = Column(JSON)
    raw_json = Column(JSON, nullable=False)
    content = Column(Text, nullable=False)

    # for OpenAI text-embedding-3-small
    embedding = Column(Vector(1536))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())