"""
benchmark_scenarios.py
======================
Scientific Model Benchmarking System.

Evaluates the trained habitability model against standardized planetary 
profiles to validate scientific consistency and edge-case performance.
"""

import os
import joblib
import pandas as pd
import numpy as np
from src.config.config import config
from src.utils.logger import setup_logger

logger = setup_logger("BenchmarkEvaluator")

SCENARIOS = {
    "Earth_Baseline": {
        "planet_radius": 1.0,
        "planet_mass": 1.0,
        "planet_density": 5.51,
        "equilibrium_temperature": 288.0,
        "stellar_temperature": 5778.0,
        "stellar_mass": 1.0,
        "stellar_radius": 1.0
    },
    "Hot_Jupiter_Extreme": {
        "planet_radius": 11.2,
        "planet_mass": 317.8,
        "planet_density": 1.33,
        "equilibrium_temperature": 1500.0,
        "stellar_temperature": 6000.0,
        "stellar_mass": 1.2,
        "stellar_radius": 1.5
    },
    "Cold_Mars_Analogue": {
        "planet_radius": 0.53,
        "planet_mass": 0.107,
        "planet_density": 3.93,
        "equilibrium_temperature": 210.0,
        "stellar_temperature": 5778.0,
        "stellar_mass": 1.0,
        "stellar_radius": 1.0
    },
    "Super_Earth_Candidate": {
        "planet_radius": 1.5,
        "planet_mass": 5.0,
        "planet_density": 6.5,
        "equilibrium_temperature": 300.0,
        "stellar_temperature": 4500.0, # M-Dwarf
        "stellar_mass": 0.5,
        "stellar_radius": 0.5
    },
    "Water_World_Candidate": {
        "planet_radius": 2.2,
        "planet_mass": 8.5,
        "planet_density": 3.2, # Lower density implies high volatile content
        "equilibrium_temperature": 350.0,
        "stellar_temperature": 5200.0,
        "stellar_mass": 0.8,
        "stellar_radius": 0.8
    }
}

def run_benchmarks():
    logger.info("Initializing Scientific Benchmark Evaluation...")
    
    # 1. Load trained model
    if not os.path.exists(config.MODEL_PATH):
        logger.error(f"Model artifact not found at {config.MODEL_PATH}. Run training pipeline first.")
        return

    artifact = joblib.load(config.MODEL_PATH)
    pipeline = artifact.get("pipeline")
    features_list = artifact.get("features", config.FEATURE_LIST)
    
    # 2. Prepare scenario dataframe
    df_scenarios = pd.DataFrame.from_dict(SCENARIOS, orient='index')
    X_bench = df_scenarios[features_list]
    
    # 3. Execute Inference
    predictions = pipeline.predict(X_bench)
    
    # 4. Compile Results
    results_df = df_scenarios.copy()
    results_df["predicted_habitability_index"] = predictions
    
    # 5. Scientific Validation Logic
    results_df["validation_status"] = "PASSED"
    # Earth should have a high score (usually > 0.8 after normalization)
    if results_df.loc["Earth_Baseline", "predicted_habitability_index"] < 0.5:
        results_df.loc["Earth_Baseline", "validation_status"] = "WARNING: Low Earth Score"
    
    # Hot Jupiter should have a very low score
    if results_df.loc["Hot_Jupiter_Extreme", "predicted_habitability_index"] > 0.3:
        results_df.loc["Hot_Jupiter_Extreme", "validation_status"] = "WARNING: High Hot Jupiter Score"

    # 6. Persist Benchmarks
    output_path = os.path.join("benchmarks", "scenarios_evaluation_summary.csv")
    results_df.to_csv(output_path)
    
    logger.info(f"Benchmark evaluation complete. Results saved to {output_path}")
    print("\n--- Benchmark Results Summary ---")
    print(results_df[["predicted_habitability_index", "validation_status"]])
    print("---------------------------------\n")
    
    return results_df

if __name__ == "__main__":
    run_benchmarks()
