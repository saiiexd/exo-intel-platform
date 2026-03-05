"""
planet_discovery_engine.py
==========================
ExoIntel – Phase 3: Planet Discovery and Ranking Engine

This script automates the discovery of potentially habitable exoplanets by combining
machine learning predictions with engineered astrophysical scores.

Workflow:
1. Loads the enriched dataset (from Phase 2).
2. Runs the trained ML model inference across all planets.
3. Computes a Combined Discovery Score (60% ML + 40% Earth Similarity).
4. Ranks candidates and computes percentile standing.
5. Saves the resulting discovery catalogue to PostgreSQL.
6. Generates visual analytics (Top 20 rankings, scatter plots, heatmaps).

Usage (from project root):
    python -m src.discovery.planet_discovery_engine
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

# Support running from root path
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

MODEL_PATH = os.path.join(_src, "ml_models", "habitability_model.pkl")

# ML model expected features
FEATURES = [
    "planet_radius", "planet_mass", "planet_density",
    "equilibrium_temperature", "stellar_temperature",
    "stellar_mass", "stellar_radius"
]


def load_enriched_data():
    print("\n[1/5] Loading Enriched Data from DB ...")
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    
    # Drop rows with nulls in features necessary for ML prediction
    original_len = len(df)
    df = df.dropna(subset=FEATURES)
    print(f"      Loaded {len(df):,} planets (dropped {original_len - len(df):,} due to missing ML features).")
    return df


def generate_ml_predictions(df):
    print("\n[2/5] Running Batch ML Inference ...")
    
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model artifact not found at {MODEL_PATH}")
        
    artifact = joblib.load(MODEL_PATH)
    model = artifact.get("pipeline", artifact)
    features_list = artifact.get("features", FEATURES)
    
    # Ensure correct feature order as trained
    X_pred = df[features_list]
    
    # Run predictions and clamp
    raw_preds = model.predict(X_pred)
    df["ml_habitability_score"] = np.clip(raw_preds, 0.0, 1.0)
    
    print(f"      Generated predictions for {len(df):,} planets.")
    return df


def rank_candidates(df):
    print("\n[3/5] Computing Ranks and Combined Scores ...")
    
    # Combined Discovery Score (60% ML, 40% ESS approx)
    # The ESS was engineered in Phase 2
    ml_weight = 0.6
    ess_weight = 0.4
    
    df["combined_discovery_score"] = (
        (df["ml_habitability_score"] * ml_weight) + 
        (df["earth_similarity_approx"] * ess_weight)
    )
    
    # Rank them (1 is best)
    df["discovery_rank"] = df["combined_discovery_score"].rank(method="min", ascending=False).astype(int)
    
    # Percentile
    df["discovery_percentile"] = df["combined_discovery_score"].rank(pct=True) * 100
    
    # Sort the dataframe so index represents actual top-down ordering
    df = df.sort_values(by="discovery_rank").reset_index(drop=True)
    
    print("      Top 5 Candidates Found:")
    for i, row in df.head(5).iterrows():
        print(f"        #{row['discovery_rank']} | {row['planet_name']:<20} | Score: {row['combined_discovery_score']:.3f} (ML: {row['ml_habitability_score']:.3f})")
        
    return df


def generate_visuals(df):
    print("\n[4/5] Generating Visual Discovery Analytics ...")
    
    # 05_top_20_candidates.png
    top_20 = df.head(20).copy()
    top_20 = top_20.sort_values(by="combined_discovery_score", ascending=True) # for horizontal bar chart
    
    plt.figure(figsize=(12, 8))
    sns.barplot(
        x="combined_discovery_score", 
        y="planet_name", 
        data=top_20,
        palette="viridis"
    )
    plt.title("Top 20 Habitable Exoplanet Candidates")
    plt.xlabel("Combined Discovery Score")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "05_top_20_candidates.png"))
    plt.close()
    
    # 06_ml_vs_ess_scatter.png
    plt.figure(figsize=(9, 7))
    sns.scatterplot(
        x="earth_similarity_approx", 
        y="ml_habitability_score", 
        hue="stellar_habitability_factor",
        size="combined_discovery_score",
        sizes=(20, 200),
        palette="magma",
        alpha=0.8,
        data=df
    )
    # Add a y=x consensus line
    plt.plot([0, 1], [0, 1], 'k--', lw=1, alpha=0.5)
    plt.title("ML Prediction Consensus vs. Physical Similarity")
    plt.xlabel("Earth Similarity Score (ESS)")
    plt.ylabel("ML-Predicted Habitability Score")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "06_ml_vs_ess_scatter.png"))
    plt.close()
    
    # 07_discovery_correlations.png
    cols_to_corr = [
        "planet_radius", "planet_mass", "equilibrium_temperature",
        "stellar_temperature", "stellar_mass",
        "earth_similarity_approx", "stellar_habitability_factor",
        "ml_habitability_score", "combined_discovery_score"
    ]
    plt.figure(figsize=(10, 8))
    corr = df[cols_to_corr].corr()
    sns.heatmap(corr, annot=True, cmap="YlGnBu", fmt=".2f")
    plt.title("Correlation Heatmap: Discovery Engine Metrics")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "07_discovery_correlations.png"))
    plt.close()
    
    print(f"      Saved 3 plots to '{OUT_DIR}'.")


def save_candidates_to_db(df):
    print("\n[5/5] Writing Discovery Results to PostgreSQL ...")
    engine = get_engine()
    
    try:
        df.to_sql(
            name="habitable_planet_candidates",
            schema="exoplanet_data",
            con=engine,
            if_exists="replace",
            index=False
        )
        print("      Successfully wrote 'exoplanet_data.habitable_planet_candidates' to DB.")
    except Exception as e:
        print(f"      Error writing to database: {e}")


def main():
    print("=" * 65)
    print("  ExoIntel – Phase 3: Planet Discovery & Ranking Engine")
    print("=" * 65)
    
    df_raw = load_enriched_data()
    df_scored = generate_ml_predictions(df_raw)
    df_ranked = rank_candidates(df_scored)
    
    generate_visuals(df_ranked)
    save_candidates_to_db(df_ranked)
    
    print("\n✅ Phase 3 Complete. The AI Discovery Catalogue is fully built.")
    print("=" * 65)


if __name__ == "__main__":
    main()
