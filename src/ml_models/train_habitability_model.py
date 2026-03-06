"""
train_habitability_model.py
===========================
ExoIntel – Robust Habitability Score Prediction Pipeline

Fixes the "Constant Prediction" issue by:
1. Extrem outlier removal (physical bounds).
2. Data balancing (downsampling major class 0.99).
3. Multi-model evaluation (RF, GBR, HistGBR).
4. Prediction variance validation.
5. Target scaling to [0, 1].

Output:
    src/ml_models/habitability_model.pkl   <- { "pipeline": p, "features": f, "y_scaler": s }
"""

import os
import sys
import warnings
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, MinMaxScaler

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("ModelTraining")
warnings.filterwarnings("ignore")

# CONFIGURATION
FEATURES = [
    "planet_radius", "planet_mass", "planet_density",
    "equilibrium_temperature", "stellar_temperature",
    "stellar_mass", "stellar_radius"
]
TARGET = "habitability_index"

def load_data():
    logger.info("Loading data from PostgreSQL...")
    engine = get_engine()
    cols = ", ".join(FEATURES + [TARGET])
    df = pd.read_sql(f"SELECT {cols} FROM exoplanet_data.planets", engine)
    logger.info(f"Loaded {len(df)} rows.")
    return df

def clean_and_balance(df):
    logger.info("Cleaning and balancing data...")
    df = df[df["stellar_mass"] < 50]
    df = df[df["stellar_radius"] < 50]
    df = df[df["planet_radius"] > 0]
    for col in ["planet_mass", "planet_density", "equilibrium_temperature"]:
        df[col] = df[col].replace(0, np.nan)
    df = df.dropna(subset=[TARGET])
    
    major_value = 0.99
    is_major = (df[TARGET] - major_value).abs() < 1e-4
    df_major = df[is_major]
    df_minor = df[~is_major]
    
    sample_size = min(max(int(len(df_major) * 0.1), len(df_minor) * 2), len(df_major))
    df_major_sampled = df_major.sample(n=sample_size, random_state=42)
    df_balanced = pd.concat([df_major_sampled, df_minor]).sample(frac=1, random_state=42)
    
    y_scaler = MinMaxScaler()
    df_balanced[TARGET] = y_scaler.fit_transform(df_balanced[[TARGET]])
    logger.info("Data cleaned and balanced.")
    return df_balanced, y_scaler

def train_best_model(df):
    logger.info("Comparing models and tuning...")
    X = df[FEATURES]
    y = df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "RandomForest": RandomForestRegressor(random_state=42),
        "GradientBoosting": GradientBoostingRegressor(random_state=42),
        "HistGradientBoosting": HistGradientBoostingRegressor(random_state=42)
    }
    
    best_name = ""
    best_score = -float("inf")
    best_model = None
    
    for name, model in models.items():
        pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("regressor", model)
        ])
        pipe.fit(X_train, y_train)
        score = pipe.score(X_test, y_test)
        preds = pipe.predict(X_test)
        var = np.std(preds)
        
        if score > best_score and var > 0.001:
            best_score = score
            best_name = name
            best_model = pipe
            
    logger.info(f"Selected Best Model: {best_name} (R2: {best_score:.4f})")
    
    param_grid = {}
    if best_name == "RandomForest":
        param_grid = {"regressor__n_estimators": [100], "regressor__max_depth": [10]}
    elif best_name == "GradientBoosting":
        param_grid = {"regressor__n_estimators": [100], "regressor__learning_rate": [0.1]}
        
    grid = GridSearchCV(best_model, param_grid, cv=3, scoring="r2", n_jobs=-1)
    grid.fit(X_train, y_train)
    return grid.best_estimator_, X_test, y_test

def evaluate(model, X_test, y_test):
    logger.info("Running Final Evaluation...")
    preds = model.predict(X_test)
    r2 = r2_score(y_test, preds)
    pred_std = np.std(preds)
    logger.info(f"Model Eval -> R2: {r2:.4f}, PredStd: {pred_std:.4f}")
    if pred_std < 0.005:
        logger.warning("Model has collapsed to a constant predictor!")

def main():
    logger.info("Starting Model Training Pipeline")
    df = load_data()
    df_balanced, y_scaler = clean_and_balance(df)
    best_pipe, X_test, y_test = train_best_model(df_balanced)
    evaluate(best_pipe, X_test, y_test)
    
    artifact = {
        "pipeline": best_pipe,
        "features": FEATURES,
        "y_scaler": y_scaler
    }
    joblib.dump(artifact, config.MODEL_PATH)
    logger.info(f"Model saved to {config.MODEL_PATH}")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()