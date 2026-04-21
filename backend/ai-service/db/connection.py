import os
from contextlib import contextmanager
import psycopg2
from psycopg2.pool import ThreadedConnectionPool
from dotenv import load_dotenv

load_dotenv()

_pool: ThreadedConnectionPool | None = None


def _normalize_dsn(database_url: str) -> str:
    """Convert SQLAlchemy URLs into psycopg2-compatible DSN URLs."""
    if database_url.startswith("postgresql+psycopg2://"):
        return "postgresql://" + database_url[len("postgresql+psycopg2://") :]
    return database_url


def get_pool() -> ThreadedConnectionPool:
    global _pool
    if _pool is None:
        raw_database_url = os.environ["DATABASE_URL"]
        _pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=_normalize_dsn(raw_database_url),
        )
    return _pool


@contextmanager
def get_connection():
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)