CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rental_listings (
    id BIGSERIAL PRIMARY KEY,
    external_id TEXT UNIQUE,
    source TEXT NOT NULL DEFAULT 'rentcast',

    formatted_address TEXT,
    city TEXT,
    state TEXT,
    zip_code TEXT,

    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,

    property_type TEXT,
    bedrooms NUMERIC(4,1),
    bathrooms NUMERIC(4,1),
    square_footage INTEGER,
    lot_size INTEGER,
    year_built INTEGER,

    price INTEGER,
    status TEXT,
    listed_date TIMESTAMP NULL,
    removed_date TIMESTAMP NULL,

    listing_url TEXT,
    image_url TEXT,

    description TEXT,
    raw_json JSONB NOT NULL,

    searchable_text TEXT NOT NULL,
    embedding VECTOR(1536),

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_rental_city_state
ON rental_listings(city, state);

CREATE INDEX IF NOT EXISTS idx_rental_price
ON rental_listings(price);

CREATE INDEX IF NOT EXISTS idx_rental_bedrooms
ON rental_listings(bedrooms);

CREATE INDEX IF NOT EXISTS idx_rental_property_type
ON rental_listings(property_type);

CREATE INDEX IF NOT EXISTS idx_rental_raw_json
ON rental_listings USING GIN(raw_json);

CREATE INDEX IF NOT EXISTS idx_rental_embedding_cosine
ON rental_listings
USING hnsw (embedding vector_cosine_ops);