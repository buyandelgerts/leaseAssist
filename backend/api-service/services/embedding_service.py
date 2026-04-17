import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in .env")

client = OpenAI(api_key=OPENAI_API_KEY)


def get_embedding(text: str) -> list[float]:
    clean_text = text.strip()
    if not clean_text:
        return []

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=clean_text,
    )
    return response.data[0].embedding