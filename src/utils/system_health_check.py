"""
system_health_check.py
======================
Diagnostic utility for verifying the integrity of the ExoIntel platform.
Checks database connectivity, schema availability, and required artifacts.
"""

import os
import sys
from sqlalchemy import create_engine, inspect
from src.config.config import config
from src.utils.logger import setup_logger

logger = setup_logger("HealthCheck")

def check_database():
    """Verifies DB connection and presence of raw data."""
    try:
        engine = create_engine(config.DATABASE_URL)
        inspector = inspect(engine)
        
        # Ensure schema exists (implicitly checked by connection if using default schema, 
        # but we check tables in exoplanet_data)
        tables = inspector.get_table_names(schema='exoplanet_data')
        
        if not tables:
             return "FAIL", "Database connected but no tables found in 'exoplanet_data' schema."
             
        if 'planets' in tables:
            return "PASS", "Database and raw 'planets' table found."
        else:
            return "FAIL", "Raw table 'exoplanet_data.planets' is missing."
    except Exception as e:
        return "FAIL", f"Database connection failed: {str(e)}"

def check_model():
    """Confirms model artifact existence."""
    if os.path.exists(config.MODEL_PATH):
        return "PASS", f"Model artifact found."
    else:
        return "WARN", "Model artifact missing (expected if running pipeline for first time)."

def check_outputs():
    """Confirms analysis outputs directory existence."""
    if not os.path.exists(config.OUTPUT_DIR):
        try:
            os.makedirs(config.OUTPUT_DIR, exist_ok=True)
            return "PASS", f"Created output directory at {config.OUTPUT_DIR}"
        except Exception as e:
            return "FAIL", f"Could not create output directory: {str(e)}"
    return "PASS", "Output directory ready."

def run_health_check():
    """Executes all health checks and returns status."""
    logger.info("Starting System Health Check...")
    
    results = {
        "Database": check_database(),
        "ML Model": check_model(),
        "Outputs": check_outputs()
    }
    
    overall_pass = True
    print("\nExoIntel System Health Diagnostic Summary:")
    print("-" * 50)
    for component, (status, message) in results.items():
        log_msg = f"[{status}] {component}: {message}"
        print(log_msg)
        if status == "FAIL":
            logger.error(log_msg)
            overall_pass = False
        else:
            logger.info(log_msg)
    print("-" * 50)
    
    if overall_pass:
        logger.info("System Health Check: PASSED")
        return True
    else:
        logger.error("System Health Check: FAILED")
        return False

if __name__ == "__main__":
    if not run_health_check():
        sys.exit(1)
