from fastapi import FastAPI
from .db import Base, engine
from .routes import listings, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rental AI Search API")

app.include_router(listings.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"message": "Rental AI Search API is running"}