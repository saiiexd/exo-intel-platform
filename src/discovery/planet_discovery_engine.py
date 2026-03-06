"""
planet_discovery_engine.py
==========================
Target Prioritization and Planet Discovery Engine.

Automates the identification of potentially habitable exoplanets by synthesizing 
machine learning predictions with astrophysical analytical indices. This module 
ranks planetary candidates using a weighted discovery score and maintains the 
primary prioritized discovery catalog.

Workflow:
1. Retrieval of curated astronomical data.
2. Gradient Boosting inference execution.
3. Composite Discovery Score computation (ML precision joined with Earth Similarity).
4. Statistical ranking and percentile standing analysis.
5. Catalog persistence and visual prioritization reporting.
"""

import os
import sys
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import joblib

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("DiscoveryEngine")
warnings.filterwarnings("ignore")

# ML model expected features
FEATURES = config.FEATURE_LIST


def load_enriched_data():
    logger.info("Loading Enriched Data from DB ...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    
    original_len = len(df)
    df = df.dropna(subset=FEATURES)
    logger.info(f"Loaded {len(df):,} planets (dropped {original_len - len(df):,} due to missing ML features).")
    return df


def generate_ml_predictions(df):
    logger.info("Running Batch ML Inference ...")
    
    if not os.path.exists(config.MODEL_PATH):
        raise FileNotFoundError(f"Model artifact not found at {config.MODEL_PATH}")
        
    artifact = joblib.load(config.MODEL_PATH)
    model = artifact.get("pipeline", artifact)
    features_list = artifact.get("features", FEATURES)
    
    X_pred = df[features_list]
    raw_preds = model.predict(X_pred)
    df["ml_habitability_score"] = np.clip(raw_preds, 0.0, 1.0)
    
    logger.info(f"Generated predictions for {len(df):,} planets.")
    return df


def rank_candidates(df):
    logger.info("Computing Ranks and Combined Scores ...")
    ml_weight, ess_weight = 0.6, 0.4
    
    df["combined_discovery_score"] = (
        (df["ml_habitability_score"] * ml_weight) + 
        (df["earth_similarity_approx"] * ess_weight)
    )
    df["discovery_rank"] = df["combined_discovery_score"].rank(method="min", ascending=False).astype(int)
    df["discovery_percentile"] = df["combined_discovery_score"].rank(pct=True) * 100
    df = df.sort_values(by="discovery_rank").reset_index(drop=True)
    
    logger.info("Discovery ranking complete.")
    return df


def generate_visuals(df):
    logger.info("Generating Visual Discovery Analytics ...")
    
    # Top 20 Candidates
    top_20 = df.head(20).copy().sort_values(by="combined_discovery_score", ascending=True)
    plt.figure(figsize=(12, 8))
    sns.barplot(x="combined_discovery_score", y="planet_name", data=top_20, palette="viridis")
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "05_top_20_candidates.png"))
    plt.close()
    
    # ML vs ESS Scatter
    plt.figure(figsize=(9, 7))
    sns.scatterplot(x="earth_similarity_approx", y="ml_habitability_score", hue="stellar_habitability_factor", data=df)
    plt.savefig(os.path.join(config.OUTPUT_DIR, "06_ml_vs_ess_scatter.png"))
    plt.close()
    
    # Correlation Heatmap
    cols = ["planet_radius", "planet_mass", "equilibrium_temperature", "ml_habitability_score", "combined_discovery_score"]
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[cols].corr(), annot=True, cmap="YlGnBu")
    plt.savefig(os.path.join(config.OUTPUT_DIR, "07_discovery_correlations.png"))
    plt.close()
    
    logger.info(f"Discovery visuals saved to {config.OUTPUT_DIR}")


def save_candidates_to_db(df):
    logger.info("Writing Discovery Results to PostgreSQL ...")
    engine = get_engine()
    try:
        df.to_sql(name="habitable_planet_candidates", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        logger.info("Successfully wrote 'exoplanet_data.habitable_planet_candidates' to DB.")
    except Exception as e:
        logger.error(f"Error writing to database: {e}")


def main():
    logger.info("Starting Planet Discovery Pipeline")
    df_raw = load_enriched_data()
    df_scored = generate_ml_predictions(df_raw)
    df_ranked = rank_candidates(df_scored)
    generate_visuals(df_ranked)
    save_candidates_to_db(df_ranked)
    logger.info("Planet Discovery Pipeline Complete.")


if __name__ == "__main__":
    main()
