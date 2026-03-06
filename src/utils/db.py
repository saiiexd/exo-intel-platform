from sqlalchemy import create_engine
import psycopg2
from src.config.config import config

def get_engine():
    """Return a SQLAlchemy engine pointing to the database."""
    return create_engine(config.DATABASE_URL)

def get_psycopg2_conn():
    """Return a raw psycopg2 connection using the central config."""
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        database=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD
    )
