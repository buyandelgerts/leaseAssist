from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Text, Integer, Float, JSON, TIMESTAMP
from pgvector.sqlalchemy import Vector


class Base(DeclarativeBase):
    pass


class RentalListing(Base):
    __tablename__ = "rental_listings"

    id: Mapped[int] = mapped_column(primary_key=True)
    external_id: Mapped[str | None] = mapped_column(Text, unique=True, nullable=True)
    source: Mapped[str] = mapped_column(Text, default="rentcast")

    formatted_address: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[str | None] = mapped_column(Text, nullable=True)
    zip_code: Mapped[str | None] = mapped_column(Text, nullable=True)

    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    property_type: Mapped[str | None] = mapped_column(Text, nullable=True)
    bedrooms: Mapped[float | None] = mapped_column(Float, nullable=True)
    bathrooms: Mapped[float | None] = mapped_column(Float, nullable=True)
    square_footage: Mapped[int | None] = mapped_column(Integer, nullable=True)
    lot_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    year_built: Mapped[int | None] = mapped_column(Integer, nullable=True)

    price: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str | None] = mapped_column(Text, nullable=True)
    listed_date: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)
    removed_date: Mapped[datetime | None] = mapped_column(TIMESTAMP, nullable=True)

    listing_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    searchable_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(1536), nullable=True)

    created_at: Mapped[datetime | None] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    updated_at: Mapped[datetime | None] = mapped_column(
        TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow
    )