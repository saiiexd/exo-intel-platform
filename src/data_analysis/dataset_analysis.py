"""
dataset_analysis.py
===================
Advanced Data Processing and Feature Engineering Module.

This module executes automated data cleansing and feature engineering for the ExoIntel 
platform. It performs outlier detection using physical constraints and statistical 
methods (IQR/Z-score), manages data balancing, and derives advanced astrophysical 
features critical for habitability prediction.

Process Flow:
1. Data Ingestion from PostgreSQL.
2. Statistical diagnostics and correlation analysis.
3. Multi-stage outlier filtering and data balancing.
4. Advanced feature derivation (Earth Similarity Score, Stellar Habitability Factor).
5. Persistence of enriched datasets and generation of analytical reports.
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

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("DatasetAnalysis")
warnings.filterwarnings("ignore")

FEATURES = config.FEATURE_LIST
TARGET = "habitability_index"


def load_data():
    logger.info("Loading data from exoplanet_data.planets ...")
    engine = get_engine()
    df = pd.read_sql(f"SELECT * FROM exoplanet_data.planets", engine)
    logger.info(f"Loaded {len(df):,} rows.")
    return df


def data_diagnostics(df):
    logger.info("Running Data Quality Diagnostics ...")
    
    # Missing value percentages
    num_rows = len(df)
    missing = df[FEATURES + [TARGET]].isnull().sum() / num_rows * 100
    
    # Initial Correlation Matrix Plot
    plt.figure(figsize=(10, 8))
    corr = df[FEATURES + [TARGET]].corr()
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Matrix (Raw Data)")
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "01_raw_correlation.png"))
    plt.close()


def clean_outliers(df):
    logger.info("Applying Filters and Removing Outliers ...")
    original_len = len(df)
    
    # 1. Physical Impossibility Filters
    for col in ["planet_radius", "planet_mass", "planet_density", "equilibrium_temperature"]:
        df[col] = df[col].replace(0, np.nan)
        
    df = df.dropna(subset=[TARGET])
    df = df[(df["stellar_mass"] < 50) | df["stellar_mass"].isnull()]
    df = df[(df["stellar_radius"] < 50) | df["stellar_radius"].isnull()]
    
    logger.info(f"Physical bounds applied: removed {original_len - len(df):,} rows.")
    current_len = len(df)
    
    # 2. Z-Score Filtering
    z_cols = ["planet_radius", "planet_mass", "equilibrium_temperature"]
    df_clean = df.copy()
    for col in z_cols:
        col_data = df_clean[col].dropna()
        z_scores = np.abs(stats.zscore(col_data))
        valid_indices = col_data[z_scores < 3].index
        df_clean = df_clean[df_clean[col].isnull() | df_clean.index.isin(valid_indices)]
        
    logger.info(f"Z-Score filtering applied: removed {current_len - len(df_clean):,} rows.")
    
    # 3. Handle Extreme Target Skew 
    major_v = 0.99
    is_major = (df_clean[TARGET] - major_v).abs() < 1e-4
    df_major = df_clean[is_major]
    df_minor = df_clean[~is_major]
    
    sample_size = min(max(int(len(df_major) * 0.1), len(df_minor) * 2), len(df_major))
    df_balanced = pd.concat([df_major.sample(n=sample_size, random_state=42), df_minor])
    
    logger.info(f"Data Balanced: final dataset has {len(df_balanced):,} rows.")
    return df_balanced


def engineer_features(df):
    logger.info("Engineering Scientifically Meaningful Features ...")
    df_eng = df.copy()
    
    # Earth Similarity Score (ESS) approximation
    r_diff = ((df_eng["planet_radius"] - 1.0) / 1.0) ** 2
    m_diff = ((df_eng["planet_mass"] - 1.0) / 1.0) ** 2
    t_diff = ((df_eng["equilibrium_temperature"] - 288) / 288) ** 2
    df_eng["earth_similarity_approx"] = 1.0 / (1.0 + np.sqrt(r_diff + m_diff + t_diff))
    df_eng["earth_similarity_approx"] = df_eng["earth_similarity_approx"].fillna(0)
    
    # Stellar Habitability Factor
    st_diff = ((df_eng["stellar_temperature"] - 5500) / 5500) ** 2
    sm_diff = ((df_eng["stellar_mass"] - 1.0) / 1.0) ** 2
    df_eng["stellar_habitability_factor"] = 1.0 / (1.0 + np.sqrt(st_diff + sm_diff))
    df_eng["stellar_habitability_factor"] = df_eng["stellar_habitability_factor"].fillna(0)
    
    # Normalized Planetary Density Ratio
    df_eng["density_ratio"] = df_eng["planet_density"] / 5.51
    df_eng["density_ratio"] = df_eng["density_ratio"].fillna(0)
    
    logger.info("Features engineered successfully.")
    return df_eng


def generate_visual_reports(df):
    logger.info("Generating Visual Reports ...")
    
    # Distribution Plot
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    sns.histplot(df["planet_radius"].dropna(), bins=40, ax=axes[0], color='skyblue')
    sns.histplot(df["planet_mass"].dropna(), bins=40, ax=axes[1], color='salmon')
    sns.histplot(df["equilibrium_temperature"].dropna(), bins=40, ax=axes[2], color='lightgreen')
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "02_parameter_distributions.png"))
    plt.close()
    
    # Scatter plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x=df["earth_similarity_approx"], y=df[TARGET], hue=df["stellar_habitability_factor"], palette="viridis")
    plt.savefig(os.path.join(config.OUTPUT_DIR, "03_earth_similarity_scatter.png"))
    plt.close()
    
    # Correlation Plot
    plt.figure(figsize=(8, 6))
    sns.heatmap(df[["earth_similarity_approx", "stellar_habitability_factor", "density_ratio", TARGET]].corr(), annot=True, cmap="mako")
    plt.savefig(os.path.join(config.OUTPUT_DIR, "04_engineered_correlation.png"))
    plt.close()
    
    logger.info(f"Visual reports saved to {config.OUTPUT_DIR}")


def save_to_database(df):
    logger.info("Writing Enriched Dataset to PostgreSQL ...")
    engine = get_engine()
    try:
        df.to_sql(name="planets_enriched", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        logger.info("Successfully wrote 'exoplanet_data.planets_enriched' to the database.")
    except Exception as e:
        logger.error(f"Error writing to database: {e}")


def main():
    logger.info("Starting Dataset Intelligence Pipeline")
    df_raw = load_data()
    data_diagnostics(df_raw)
    df_cleaned = clean_outliers(df_raw)
    df_enriched = engineer_features(df_cleaned)
    generate_visual_reports(df_enriched)
    save_to_database(df_enriched)
    logger.info("Dataset Intelligence Pipeline Complete.")

if __name__ == "__main__":
    main()
