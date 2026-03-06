"""
ingest_exoplanet_data.py
========================
Data Acquisition and Ingestion Module.

Retrieves raw planetary datasets from the NASA Exoplanet Archive TAP service 
and synchronizes them with the PostgreSQL data warehouse.
"""

import requests
import json
from src.config.config import config
from src.utils.db import get_psycopg2_conn
from src.utils.logger import setup_logger

logger = setup_logger("Injestor")

# NASA dataset TAP API
NASA_TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,discoverymethod,disc_year,pl_orbper,pl_rade,pl_bmasse,pl_eqt,st_teff,st_mass,st_rad+from+pscomppars&format=json"

def ingest_data():
    logger.info("Initializing dataset acquisition from NASA Exoplanet Archive...")
    
    try:
        response = requests.get(NASA_TAP_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully retrieved {len(data):,} planetary records.")
    except Exception as e:
        logger.error(f"Failed to retrieve data from NASA Archive: {e}")
        return

    logger.info("Establishing connection to PostgreSQL warehouse...")
    try:
        conn = get_psycopg2_conn()
        cursor = conn.cursor()
    except Exception as e:
        logger.error(f"Database connection failure: {e}")
        return

    # Using ON CONFLICT (planet_name) requires a primary key or unique constraint on planet_name.
    # We assume the schema is set up correctly for this.
    insert_query = """
    INSERT INTO exoplanet_data.planets 
    (planet_name, host_star, discovery_method, discovery_year, 
    orbital_period, planet_radius, planet_mass, equilibrium_temperature, 
    stellar_temperature, stellar_mass, stellar_radius) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (planet_name) DO UPDATE SET
        host_star = EXCLUDED.host_star,
        discovery_method = EXCLUDED.discovery_method,
        orbital_period = EXCLUDED.orbital_period;
    """

    logger.info("Synchronizing data warehouse records...")
    insert_count = 0
    for planet in data:
        values = (
            planet.get("pl_name"),
            planet.get("hostname"),
            planet.get("discoverymethod"),
            planet.get("disc_year"),
            planet.get("pl_orbper"),
            planet.get("pl_rade"),
            planet.get("pl_bmasse"),
            planet.get("pl_eqt"),
            planet.get("st_teff"),
            planet.get("st_mass"),
            planet.get("st_rad")
        )
        try:
            cursor.execute(insert_query, values)
            insert_count += 1
        except Exception:
            conn.rollback()
            continue

    conn.commit()
    logger.info(f"Synchronization complete. Total records processed: {insert_count:,}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    ingest_data()