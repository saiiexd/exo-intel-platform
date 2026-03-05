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
import sys
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

_here = os.path.dirname(os.path.abspath(__file__))
_src = os.path.dirname(_here)
_root = os.path.dirname(_src)
if _src not in sys.path:
    sys.path.insert(0, _src)
if _root not in sys.path:
    sys.path.insert(0, _root)

from utils.db import get_engine

warnings.filterwarnings("ignore")

OUT_DIR = os.path.join(_root, "analysis_outputs")
os.makedirs(OUT_DIR, exist_ok=True)

def generate_insights():
    print("=" * 65)
    print("  ExoIntel – Phase 6: Scientific Insight Engine")
    print("=" * 65)
    
    engine = get_engine()
    
    print("\n[1/4] Loading Datasets from PostgreSQL ...")
    df_enriched = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    df_candidates = pd.read_sql("SELECT * FROM exoplanet_data.habitable_planet_candidates", engine)
    
    # Merge ML predictions onto the full enriched dataset
    # This ensures we retain the discovery_method and all raw data
    merge_cols = ["planet_name", "ml_habitability_score", "combined_discovery_score", "discovery_rank"]
    df = pd.merge(df_enriched, df_candidates[merge_cols], on="planet_name", how="inner")
    
    print(f"      Loaded {len(df):,} planets with ML predictions.")
    
    print("\n[2/4] Computing Analytical Summaries ...")
    
    # 1. Discovery Method Analysis
    discovery_analysis = df.groupby("discovery_method").agg(
        planet_count=("planet_name", "count"),
        avg_ml_habitability=("ml_habitability_score", "mean"),
        max_ml_habitability=("ml_habitability_score", "max")
    ).reset_index().sort_values("avg_ml_habitability", ascending=False)
    
    # 2. Stellar & Planetary Habitability Patterns 
    # Binning constraints to find patterns
    df["radius_category"] = pd.cut(df["planet_radius"], bins=[0, 1.5, 2.5, 10, np.inf], 
                                   labels=["Earth-size", "Super-Earth", "Neptune-like", "Gas Giant"])
    df["stellar_temp_category"] = pd.cut(df["stellar_temperature"], bins=[0, 3500, 5000, 6000, np.inf],
                                         labels=["M-Dwarf (Cool)", "K-Dwarf", "G-Type (Sun-like)", "F/A-Type (Hot)"])
    
    stellar_patterns = df.groupby(["radius_category", "stellar_temp_category"]).agg(
        planet_count=("planet_name", "count"),
        avg_habitability=("ml_habitability_score", "mean")
    ).dropna().reset_index()
    
    # 3. Multi-Planet Habitable Systems
    # Identify systems with more than 1 planet having ML Score > 0.6
    habitable_threshold = 0.6
    hab_sys = df[df["ml_habitability_score"] > habitable_threshold]
    system_counts = hab_sys.groupby("host_star").size().reset_index(name="habitable_planet_count")
    multi_planet_systems = system_counts[system_counts["habitable_planet_count"] > 1]
    
    # Get details of these planets
    multi_planet_details = pd.merge(multi_planet_systems, hab_sys, on="host_star")
    multi_planet_export = multi_planet_details[["host_star", "habitable_planet_count", "planet_name", "ml_habitability_score", "planet_radius", "equilibrium_temperature"]].sort_values(["habitable_planet_count", "host_star", "ml_habitability_score"], ascending=[False, True, False])
    
    print(f"      Found {len(multi_planet_systems)} star systems hosting multiple potentially habitable planets.")
    
    print("\n[3/4] Exporting Insights to PostgreSQL ...")
    try:
        discovery_analysis.to_sql("discovery_method_analysis", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        stellar_patterns.to_sql("stellar_habitability_patterns", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        multi_planet_export.to_sql("multi_planet_habitable_systems", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        print("      Successfully wrote structural insight tables to the database.")
    except Exception as e:
        print(f"      Database write failed: {e}")
        
    print("\n[4/4] Generating Visual Analysis Reports ...")
    
    # Plot 1: Habitability vs Stellar Temperature Scatter
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        data=df, x="stellar_temperature", y="ml_habitability_score", 
        hue="radius_category", size="planet_radius",
        sizes=(20, 200), alpha=0.7, palette="flare"
    )
    plt.title("Habitability Score vs Stellar Temperature")
    plt.xlabel("Stellar Temperature (K)")
    plt.ylabel("ML Habitability Score")
    plt.axvspan(5000, 6000, color='green', alpha=0.1, label='Sun-like Zone')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "11_habitability_vs_stellar_temp.png"))
    plt.close()
    
    # Plot 2: Average Habitability by Discovery Method
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=discovery_analysis.head(10), x="avg_ml_habitability", y="discovery_method", palette="Blues_r"
    )
    plt.title("Average Habitability Score by Discovery Method")
    plt.xlabel("Average ML Score")
    plt.ylabel("Discovery Method")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "12_habitability_by_discovery_method.png"))
    plt.close()
    
    # Plot 3: Histogram Distribution of Habitability Scores
    plt.figure(figsize=(9, 5))
    sns.histplot(df["ml_habitability_score"], bins=50, kde=True, color="purple")
    plt.title("Distribution of ML Habitability Scores Across Galaxy")
    plt.xlabel("ML Habitability Score")
    plt.ylabel("Number of Planets")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "13_habitability_score_distribution.png"))
    plt.close()
    
    # Plot 4: Heatmap Correlation Matrix
    numeric_cols = [
        "planet_radius", "planet_mass", "planet_density", 
        "equilibrium_temperature", "stellar_temperature", "stellar_mass", 
        "earth_similarity_approx", "stellar_habitability_factor", "ml_habitability_score"
    ]
    plt.figure(figsize=(11, 9))
    corr = df[numeric_cols].corr()
    sns.heatmap(corr, annot=True, cmap="Spectral_r", fmt=".2f", vmin=-1, vmax=1)
    plt.title("Scientific Insight: Planetary Metrics & Habitability Correlation")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "14_insight_correlation_heatmap.png"))
    plt.close()
    
    print(f"      Saved 4 analytical plots to '{OUT_DIR}'.")
    print("\n✅ Phase 6 Complete. Scientific Insight Engine finished.")
    print("=" * 65)

if __name__ == "__main__":
    generate_insights()
