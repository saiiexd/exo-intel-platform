from sqlalchemy import create_engine
import psycopg2

# Centralized database configuration
CONNECTION_STRING = "postgresql://postgres:saivenkat143@localhost/exo_intel_db"


def get_engine():
    """Return a SQLAlchemy engine pointing to the exo_intel_db database."""
    return create_engine(CONNECTION_STRING)


def get_psycopg2_conn():
    """Return a raw psycopg2 connection using the same credentials."""
    return psycopg2.connect(
        host="localhost",
        database="exo_intel_db",
        user="postgres",
        password="saivenkat143"
    )
