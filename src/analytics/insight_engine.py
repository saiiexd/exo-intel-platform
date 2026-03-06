"""
insight_engine.py
=================
ExoIntel – Phase 6: Scientific Insight Engine

Automatically analyzes the enriched dataset and discovery results to surface
scientific insights about planetary habitability trends across the galaxy.

Usage:
    python -m src.analytics.insight_engine
"""
import os
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("InsightEngine")
warnings.filterwarnings("ignore")

def generate_insights():
    logger.info("Starting Scientific Insight Analysis")
    engine = get_engine()
    
    logger.info("Loading Datasets from PostgreSQL ...")
    df_enriched = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    df_candidates = pd.read_sql("SELECT * FROM exoplanet_data.habitable_planet_candidates", engine)
    
    merge_cols = ["planet_name", "ml_habitability_score", "combined_discovery_score", "discovery_rank"]
    df = pd.merge(df_enriched, df_candidates[merge_cols], on="planet_name", how="inner")
    
    logger.info(f"Loaded {len(df):,} planets with ML predictions.")
    
    # 1. Discovery Method Analysis
    discovery_analysis = df.groupby("discovery_method").agg(
        planet_count=("planet_name", "count"),
        avg_ml_habitability=("ml_habitability_score", "mean")
    ).reset_index().sort_values("avg_ml_habitability", ascending=False)
    
    # 2. Stellar Patterns 
    df["radius_category"] = pd.cut(df["planet_radius"], bins=[0, 1.5, 2.5, 10, np.inf], 
                                   labels=["Earth-size", "Super-Earth", "Neptune-like", "Gas Giant"])
    stellar_patterns = df.groupby("radius_category").agg(
        avg_habitability=("ml_habitability_score", "mean")
    ).dropna().reset_index()
    
    logger.info("Exporting Insights to PostgreSQL ...")
    try:
        discovery_analysis.to_sql("discovery_method_analysis", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        stellar_patterns.to_sql("stellar_habitability_patterns", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        logger.info("Structural insight tables saved to DB.")
    except Exception as e:
        logger.error(f"Database write failed: {e}")
        
    logger.info("Generating Visual Analysis Reports ...")
    
    # Plot 1: Habitability vs Stellar Temp
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="stellar_temperature", y="ml_habitability_score", hue="radius_category", alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "11_habitability_vs_stellar_temp.png"))
    plt.close()
    
    # Plot 2: Habitability by Discovery Method
    plt.figure(figsize=(10, 6))
    sns.barplot(data=discovery_analysis.head(10), x="avg_ml_habitability", y="discovery_method", palette="Blues_r")
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "12_habitability_by_discovery_method.png"))
    plt.close()
    
    # Plot 3: Distribution
    plt.figure(figsize=(9, 5))
    sns.histplot(df["ml_habitability_score"], bins=50, kde=True, color="purple")
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "13_habitability_score_distribution.png"))
    plt.close()
    
    # Plot 4: Correlation Heatmap
    cols = ["planet_radius", "planet_mass", "equilibrium_temperature", "ml_habitability_score"]
    plt.figure(figsize=(11, 9))
    sns.heatmap(df[cols].corr(), annot=True, cmap="Spectral_r", vmin=-1, vmax=1)
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "14_insight_correlation_heatmap.png"))
    plt.close()
    
    logger.info(f"Insight visuals saved to {config.OUTPUT_DIR}")
    logger.info("Scientific Insight Engine finished.")

if __name__ == "__main__":
    generate_insights()
