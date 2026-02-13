import psycopg2
from app.config import settings

def get_db_connection():
    """Establishes and returns a connection to the PostgreSQL database."""
    conn = psycopg2.connect(
        host=settings.DB_HOST,
        database=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD
    )
    return conn
