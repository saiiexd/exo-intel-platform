"""
experiment_orchestrator.py
==========================
Automated Research Experiment Tracking System.

Executes cross-algorithm performance benchmarks for exoplanet habitability 
prediction. Compares multiple regression architectures and persists formal 
performance metrics for scientific reproducibility.
"""

import os
import json
import time
from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.config.config import config
from src.utils.logger import setup_logger
from src.ml_models.train_habitability_model import load_data, clean_and_balance

logger = setup_logger("ExperimentOrchestrator")

def run_experiment():
    logger.info("Initializing Research Experiment Suite...")
    
    # 1. Load and Prepare Research Data
    df = load_data()
    df_balanced, _ = clean_and_balance(df)
    
    X = df_balanced[config.FEATURE_LIST]
    y = df_balanced["habitability_index"]
    
    # 80/20 train-test split for final validation metrics
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Define Algorithms for Comparison
    algorithms = {
        "LinearRegression": LinearRegression(),
        "RandomForest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
        "HistGradientBoosting": HistGradientBoostingRegressor(random_state=42)
    }
    
    results = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "n_samples": len(df_balanced),
            "features": config.FEATURE_LIST
        },
        "experiments": []
    }
    
    logger.info(f"Evaluating {len(algorithms)} baseline algorithms...")
    
    # 3. Execute Benchmarking
    for name, model in algorithms.items():
        logger.info(f"Running benchmarks for architecture: {name}")
        
        pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("regressor", model)
        ])
        
        # Perform 5-Fold Cross-Validation
        cv_results = cross_validate(
            pipe, X, y, cv=5, 
            scoring=["r2", "neg_mean_absolute_error", "neg_root_mean_squared_error"],
            return_train_score=True
        )
        
        # Fit and Evaluate on Hold-out Set
        start_time = time.time()
        pipe.fit(X_train, y_train)
        training_duration = time.time() - start_time
        
        preds = pipe.predict(X_test)
        
        exp_metrics = {
            "algorithm": name,
            "training_duration_sec": training_duration,
            "cv_metrics": {
                "r2_mean": np.mean(cv_results["test_r2"]),
                "r2_std": np.std(cv_results["test_r2"]),
                "mae_mean": -np.mean(cv_results["test_neg_mean_absolute_error"]),
                "rmse_mean": -np.mean(cv_results["test_neg_root_mean_squared_error"])
            },
            "holdout_metrics": {
                "r2": r2_score(y_test, preds),
                "mae": mean_absolute_error(y_test, preds),
                "rmse": np.sqrt(mean_squared_error(y_test, preds))
            }
        }
        
        results["experiments"].append(exp_metrics)
        logger.info(f"Finished {name}: R2={exp_metrics['holdout_metrics']['r2']:.4f}")

    # 4. Persist Experiment Results
    output_path = os.path.join("experiments", f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    
    logger.info(f"Experiment suite complete. Results archived to {output_path}")
    
    # Generate CSV summary for quick review
    summary_df = pd.DataFrame([
        {
            "Algorithm": e["algorithm"],
            "R2 (Holdout)": e["holdout_metrics"]["r2"],
            "R2 (CV Mean)": e["cv_metrics"]["r2_mean"],
            "MAE": e["holdout_metrics"]["mae"],
            "Duration": e["training_duration_sec"]
        } for e in results["experiments"]
    ])
    csv_path = os.path.join("experiments", "experiment_summary_latest.csv")
    summary_df.to_csv(csv_path, index=False)
    
    return results

if __name__ == "__main__":
    run_experiment()
