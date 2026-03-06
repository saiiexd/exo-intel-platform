"""
api/main.py
============
FastAPI Research Service for the ExoIntel Platform.

Exposes discovery results, feature importance, and planetary analytics 
via a RESTful interface for external research integration.
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
import pandas as pd
import json

from src.utils.db import get_engine
from src.config.config import config

app = FastAPI(
    title="ExoIntel Research API",
    description="Programmatic access to habitable exoplanet intelligence.",
    version="1.4.0"
)

# Database Engine
engine = get_engine()

@app.get("/health")
def health_check():
    """Confirms system and database operational status."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected", "platform": "ExoIntel v1.4.0"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/top-candidates")
def get_top_candidates(limit: int = 50):
    """Returns the top ranked habitable exoplanet candidates."""
    try:
        query = text(f"SELECT * FROM exoplanet_data.habitable_planet_candidates ORDER BY combined_discovery_score DESC LIMIT {limit}")
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/planet/{name}")
def get_planet_details(name: str):
    """Returns deep-dive analytics and predictions for a specific planet."""
    try:
        query = text("SELECT * FROM exoplanet_data.habitable_planet_candidates WHERE planet_name = :name")
        df = pd.read_sql(query, engine, params={"name": name})
        
        if df.empty:
            raise HTTPException(status_code=404, detail="Planet not found in discovery catalog.")
            
        return df.iloc[0].to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feature-importance")
def get_feature_importance():
    """Returns global SHAP feature importance rankings."""
    try:
        query = text("SELECT * FROM exoplanet_data.feature_importance_analysis ORDER BY mean_abs_shap DESC")
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/discovery-summary")
def get_discovery_summary():
    """Returns high-level discovery statistics from the latest research snapshot."""
    try:
        query = text("SELECT * FROM exoplanet_data.discovery_summary_snapshot")
        df = pd.read_sql(query, engine)
        if df.empty:
            return {"status": "No snapshot available. Run pipeline to generate."}
        return df.iloc[0].to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/pipeline")
def get_pipeline_metrics(limit: int = 10):
    """Returns the most recent pipeline execution metrics."""
    try:
        query = text(f"SELECT * FROM platform_metrics.pipeline_runs ORDER BY timestamp DESC LIMIT {limit}")
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/model")
def get_model_metrics():
    """Returns the most recent machine learning model performance metrics."""
    try:
        query = text("SELECT * FROM platform_metrics.model_performance ORDER BY timestamp DESC LIMIT 1")
        df = pd.read_sql(query, engine)
        if df.empty:
            return {"status": "No model metrics available."}
        return df.iloc[0].to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/metrics/discovery")
def get_discovery_metrics():
    """Returns historical discovery statistics snapshots."""
    try:
        query = text("SELECT * FROM platform_metrics.discovery_statistics ORDER BY timestamp DESC LIMIT 10")
        df = pd.read_sql(query, engine)
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
