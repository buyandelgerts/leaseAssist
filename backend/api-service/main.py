from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.listings import router as listings_router
from routes.search import router as search_router

app = FastAPI(title="Rental AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for local dev only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(listings_router)
app.include_router(search_router)


@app.get("/")
def root():
    return {"message": "Rental AI API is running"}