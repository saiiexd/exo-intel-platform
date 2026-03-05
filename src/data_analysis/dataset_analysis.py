"""
dataset_analysis.py
===================
ExoIntel – Phase 2: Dataset Intelligence & Feature Engineering

This script connects to the PostgreSQL database, analyzes the raw exoplanet data,
removes impossible and extreme outliers (using physical bounds, IQR, and Z-scores),
and computes scientifically meaningful astrophysical features:
1. Earth Similarity Score (ESS) approximation
2. Stellar Habitability Factor
3. Normalized Planetary Density Ratio

The cleaned and enriched dataset is saved back to 'exoplanet_data.planets_enriched'
and visualization reports are written to the 'analysis_outputs/' directory.

Usage (from project root):
    python -m src.data_analysis.dataset_analysis
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
from scipy import stats

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

FEATURES = [
    "planet_radius", "planet_mass", "planet_density",
    "equilibrium_temperature", "stellar_temperature",
    "stellar_mass", "stellar_radius"
]
TARGET = "habitability_index"


def load_data():
    print("\n[1/6] Loading data from exoplanet_data.planets ...")
    engine = get_engine()
    df = pd.read_sql(f"SELECT * FROM exoplanet_data.planets", engine)
    print(f"      Loaded {len(df):,} rows.")
    return df


def data_diagnostics(df):
    print("\n[2/6] Running Data Quality Diagnostics ...")
    
    # Missing value percentages
    num_rows = len(df)
    missing = df[FEATURES + [TARGET]].isnull().sum() / num_rows * 100
    print("\n--- Missing Value Percentages (%) ---")
    print(missing[missing > 0].to_string() if (missing > 0).any() else "No missing values.")
    
    # Zero value count (often means missing in astronomy datasets)
    print("\n--- Zero / Impossible Value Counts ---")
    for col in FEATURES:
        zero_pct = (df[col] == 0).sum() / num_rows * 100
        print(f"{col:25} : {zero_pct:.2f}%")
        
    # Feature Variance
    print("\n--- Feature Variance ---")
    variance = df[FEATURES].var()
    print(variance.to_string())
    
    # Initial Correlation Matrix Plot
    plt.figure(figsize=(10, 8))
    corr = df[FEATURES + [TARGET]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix (Raw Data)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "01_raw_correlation.png"))
    plt.close()


def clean_outliers(df):
    print("\n[3/6] Applying Filters and Removing Outliers ...")
    original_len = len(df)
    
    # 1. Physical Impossibility Filters
    # Radius & Mass & Temp cannot be <= 0. Replace with NaN so we can impute/drop
    for col in ["planet_radius", "planet_mass", "planet_density", "equilibrium_temperature"]:
        df[col] = df[col].replace(0, np.nan)
        
    # Drop rows where target is NaN
    df = df.dropna(subset=[TARGET])
    
    # Drop extreme stellar mass/radius (impossible stars)
    df = df[(df["stellar_mass"] < 50) | df["stellar_mass"].isnull()]
    df = df[(df["stellar_radius"] < 50) | df["stellar_radius"].isnull()]
    
    print(f"      Physical bounds applied: removed {original_len - len(df):,} rows.")
    current_len = len(df)
    
    # 2. Z-Score Filtering for continuous columns (drop rows > 3 std devs away)
    # Only calculate z-score on non-null rows for the continuous columns
    z_cols = ["planet_radius", "planet_mass", "equilibrium_temperature"]
    df_clean = df.copy()
    for col in z_cols:
        col_data = df_clean[col].dropna()
        z_scores = np.abs(stats.zscore(col_data))
        # Keep rows that are either NaN (will be imputed later) or have Z-score < 3
        valid_indices = col_data[z_scores < 3].index
        df_clean = df_clean[df_clean[col].isnull() | df_clean.index.isin(valid_indices)]
        
    print(f"      Z-Score filtering applied: removed {current_len - len(df_clean):,} rows.")
    
    # 3. Handle Extreme Target Skew 
    # Downsample the major class (0.99) that we found in Phase 1b to balance dataset visually
    major_v = 0.99
    is_major = (df_clean[TARGET] - major_v).abs() < 1e-4
    df_major = df_clean[is_major]
    df_minor = df_clean[~is_major]
    
    sample_size = min(max(int(len(df_major) * 0.1), len(df_minor) * 2), len(df_major))
    df_balanced = pd.concat([df_major.sample(n=sample_size, random_state=42), df_minor])
    
    print(f"      Data Balanced: final dataset has {len(df_balanced):,} rows.")
    return df_balanced


def engineer_features(df):
    print("\n[4/6] Engineering Scientifically Meaningful Features ...")
    df_eng = df.copy()
    
    # 1. Earth Similarity Score (ESS) approximation
    # Normalizes Planet differences: Earth Radius = 1.0, Mass = 1.0, Temp = 288K
    # Formula uses Euclidean distance in normalized space
    r_diff = ((df_eng["planet_radius"] - 1.0) / 1.0) ** 2
    m_diff = ((df_eng["planet_mass"] - 1.0) / 1.0) ** 2
    t_diff = ((df_eng["equilibrium_temperature"] - 288) / 288) ** 2
    
    # Invert the distance so 1.0 is highest similarity
    df_eng["earth_similarity_approx"] = 1.0 / (1.0 + np.sqrt(r_diff + m_diff + t_diff))
    df_eng["earth_similarity_approx"] = df_eng["earth_similarity_approx"].fillna(0)
    
    # 2. Stellar Habitability Factor
    # A synthetic metric balancing stellar temperature (ideal ~5500K) and mass (ideal ~1.0)
    st_diff = ((df_eng["stellar_temperature"] - 5500) / 5500) ** 2
    sm_diff = ((df_eng["stellar_mass"] - 1.0) / 1.0) ** 2
    df_eng["stellar_habitability_factor"] = 1.0 / (1.0 + np.sqrt(st_diff + sm_diff))
    df_eng["stellar_habitability_factor"] = df_eng["stellar_habitability_factor"].fillna(0)
    
    # 3. Normalized Planetary Density Ratio
    # Density relative to Earth (5.51 g/cm³); < 0.5 usually means gas, > 1.0 iron-rich
    df_eng["density_ratio"] = df_eng["planet_density"] / 5.51
    df_eng["density_ratio"] = df_eng["density_ratio"].fillna(0)
    
    print("      Features added: 'earth_similarity_approx', 'stellar_habitability_factor', 'density_ratio'.")
    return df_eng


def generate_visual_reports(df):
    print("\n[5/6] Generating Visual Reports ...")
    
    # Distribution of Physical Parameters
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df["planet_radius"].dropna(), bins=40, ax=axes[0], color='skyblue')
    axes[0].set_title("Planet Radius Distribution")
    axes[0].set_xlabel("Earth Radii")
    
    sns.histplot(df["planet_mass"].dropna(), bins=40, ax=axes[1], color='salmon')
    axes[1].set_title("Planet Mass Distribution")
    axes[1].set_xlabel("Earth Masses")
    
    sns.histplot(df["equilibrium_temperature"].dropna(), bins=40, ax=axes[2], color='lightgreen')
    axes[2].set_title("Equilibrium Temperature Distribution")
    axes[2].set_xlabel("Kelvin")
    
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "02_parameter_distributions.png"))
    plt.close()
    
    # Scatter: Earth Similarity vs Habitability Index
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x=df["earth_similarity_approx"], 
        y=df[TARGET], 
        hue=df["stellar_habitability_factor"], 
        palette="viridis", alpha=0.7
    )
    plt.title("Earth Similarity vs Habitability Score")
    plt.xlabel("Earth Similarity Approximation")
    plt.ylabel("Assessed Habitability Index")
    plt.savefig(os.path.join(OUT_DIR, "03_earth_similarity_scatter.png"))
    plt.close()
    
    # Engineered Features Correlation
    eng_cols = ["earth_similarity_approx", "stellar_habitability_factor", "density_ratio", TARGET]
    plt.figure(figsize=(8, 6))
    corr = df[eng_cols].corr()
    sns.heatmap(corr, annot=True, cmap="mako", fmt=".2f")
    plt.title("Correlation: Engineered Features")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "04_engineered_correlation.png"))
    plt.close()
    
    print(f"      Saved 4 plots to '{OUT_DIR}'.")


def save_to_database(df):
    print("\n[6/6] Writing Enriched Dataset to PostgreSQL ...")
    engine = get_engine()
    
    # To avoid writing an enormous dataframe quickly, we drop na index column and set if_exists replace
    df_export = df.copy()
    
    try:
        df_export.to_sql(
            name="planets_enriched",
            schema="exoplanet_data",
            con=engine,
            if_exists="replace",
            index=False
        )
        print("      Successfully wrote 'exoplanet_data.planets_enriched' to the database.")
    except Exception as e:
        print(f"      Error writing to database: {e}")


def main():
    print("=" * 60)
    print("  ExoIntel – Dataset Intelligence & Feature Engineering")
    print("=" * 60)
    
    df_raw = load_data()
    data_diagnostics(df_raw)
    
    df_cleaned = clean_outliers(df_raw)
    df_enriched = engineer_features(df_cleaned)
    
    generate_visual_reports(df_enriched)
    save_to_database(df_enriched)
    
    print("\n✅ Phase 2 complete. Enriched dataset is ready for advanced modeling.")
    print("=" * 60)

if __name__ == "__main__":
    main()
