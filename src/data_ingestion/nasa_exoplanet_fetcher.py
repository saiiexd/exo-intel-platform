"""
nasa_exoplanet_fetcher.py
=========================
Automated Data Ingestion Module for ExoIntel.

Retrieves the latest planetary system composite data from the NASA Exoplanet 
Archive using the TAP (Table Access Protocol) service. Normalizes data 
columns to the ExoIntel schema and persists to the PostgreSQL warehouse.
"""

import os
import requests
import pandas as pd
import io
from sqlalchemy import text
from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("DataIngestion")

# NASA Exoplanet Archive TAP Endpoint
TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# TAP Query for Comprehensive Planetary Systems Data (pscomppars)
# This table provides the most complete 'composite' set of parameters.
ADQL_QUERY = """
SELECT 
    pl_name, hostname, discoverymethod, disc_year, 
    pl_orbper, pl_rade, pl_masse, pl_dens, pl_eqt,
    st_teff, st_rad, st_mass
FROM pscomppars
"""

# Mapping NASA TAP columns to internal ExoIntel Schema
COLUMN_MAPPING = {
    "pl_name": "planet_name",
    "hostname": "host_star",
    "discoverymethod": "discovery_method",
    "disc_year": "discovery_year",
    "pl_orbper": "orbital_period",
    "pl_rade": "planet_radius",
    "pl_masse": "planet_mass",
    "pl_dens": "planet_density",
    "pl_eqt": "equilibrium_temperature",
    "st_teff": "stellar_temperature",
    "st_rad": "stellar_radius",
    "st_mass": "stellar_mass"
}

REQUIRED_COLUMNS = list(COLUMN_MAPPING.values())

def fetch_latest_nasa_data():
    logger.info("Initiating TAP query to NASA Exoplanet Archive...")
    
    params = {
        "QUERY": ADQL_QUERY,
        "FORMAT": "csv"
    }
    
    try:
        response = requests.get(TAP_URL, params=params, timeout=60)
        response.raise_for_status()
        
        logger.info("Payload received. Processing CSV data...")
        df = pd.read_csv(io.StringIO(response.text))
        
        # 1. Normalize Column Names
        df = df.rename(columns=COLUMN_MAPPING)
        
        # 2. Validation: Ensure all required columns exist
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            error_msg = f"NASA payload missing critical scientific columns: {missing}"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # 3. Validation: Check data volume
        if len(df) < 3000: # We expect ~5500+ confirmed planets
            logger.warning(f"Unexpectedly low row count: {len(df)}. NASA Archive might be undergoing maintenance.")
            
        logger.info(f"Successfully ingested {len(df):,} planetary records from NASA.")
        return df

    except Exception as e:
        logger.error(f"NASA TAP ingestion failure: {e}")
        raise

def persist_to_warehouse(df):
    logger.info("Persisting raw astronomical data to PostgreSQL...")
    engine = get_engine()
    
    try:
        # Write to planets_raw_latest table (this one doesn't have views yet, so replace is fine)
        df.to_sql(
            name="planets_raw_latest", 
            schema="exoplanet_data", 
            con=engine, 
            if_exists="replace", 
            index=False
        )
        logger.info("Successfully updated 'exoplanet_data.planets_raw_latest'.")
        
        # For 'planets', use TRUNCATE + APPEND to preserve dependent views
        with engine.begin() as conn:
            logger.info("Truncating 'exoplanet_data.planets' to preserve dependent views...")
            conn.execute(text("TRUNCATE TABLE exoplanet_data.planets CASCADE;"))
            
            # Use append to insert the new scientific observations
            df.to_sql(
                name="planets", 
                schema="exoplanet_data", 
                con=conn, 
                if_exists="append", 
                index=False
            )
            
        logger.info("Synchronized 'exoplanet_data.planets' with latest external observations via TRUNCATE/APPEND.")
        
    except Exception as e:
        logger.error(f"Database persistence failure: {e}")
        raise

if __name__ == "__main__":
    try:
        data = fetch_latest_nasa_data()
        persist_to_warehouse(data)
        logger.info("Autonomous Ingestion Stage Complete.")
    except Exception as e:
        logger.critical(f"Ingestion Module CRITICAL FAILURE: {e}")
        exit(1)
