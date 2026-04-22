CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE public.rental_listings (
	id bigserial NOT NULL,
	rentcast_id text NULL,
	formatted_address text NULL,
	city text NULL,
	state text NULL,
	zip_code text NULL,
	latitude float8 NULL,
	longitude float8 NULL,
	property_type text NULL,
	bedrooms numeric NULL,
	bathrooms numeric NULL,
	square_footage int4 NULL,
	price int4 NULL,
	status text NULL,
	listing_type text NULL,
	features jsonb NULL,
	raw_json jsonb NOT NULL,
	"content" text NOT NULL,
	embedding public.vector NULL,
	created_at timestamp DEFAULT now() NULL,
	updated_at timestamp DEFAULT now() NULL,
	CONSTRAINT rental_listings_pkey PRIMARY KEY (id),
	CONSTRAINT rental_listings_rentcast_id_key UNIQUE (rentcast_id)
);
CREATE INDEX idx_rental_bedrooms ON public.rental_listings USING btree (bedrooms);
CREATE INDEX idx_rental_city_state ON public.rental_listings USING btree (city, state);
CREATE INDEX idx_rental_price ON public.rental_listings USING btree (price);

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