"""
config.py
=========
Centralized configuration management for the ExoIntel platform.
Loads system settings and credentials from environment variables.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database Configuration
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "exo_intel_db")
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # File Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODEL_DIR = os.path.join(BASE_DIR, "src", "ml_models")
    MODEL_PATH = os.path.join(MODEL_DIR, "habitability_model.pkl")
    OUTPUT_DIR = os.path.join(BASE_DIR, "analysis_outputs")
    LOGS_DIR = os.path.join(BASE_DIR, "pipeline_logs")
    
    # Ensure directories exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(LOGS_DIR, exist_ok=True)

    # Feature Engineering Configuration
    FEATURE_LIST = [
        "planet_radius", "planet_mass", "planet_density",
        "equilibrium_temperature", "stellar_temperature",
        "stellar_mass", "stellar_radius"
    ]

config = Config()
