import os
import sys
import warnings
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import joblib
import shap

from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("ExplainabilityEngine")
warnings.filterwarnings("ignore")

def generate_explanations():
    logger.info("Starting SHAP Explainability Analysis")
    engine = get_engine()
    
    logger.info("Loading Enriched Dataset ...")
    df = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    
    if not os.path.exists(config.MODEL_PATH):
        logger.error(f"Model not found at {config.MODEL_PATH}")
        return
        
    logger.info("Loading the Trained ML Model ...")
    artifact = joblib.load(config.MODEL_PATH)
    pipeline = artifact.get("pipeline", artifact)
    features_list = artifact.get("features", [
        "planet_radius", "planet_mass", "planet_density",
        "equilibrium_temperature", "stellar_temperature",
        "stellar_mass", "stellar_radius"
    ])
        
    df = df.dropna(subset=features_list).copy().reset_index(drop=True)
    X = df[features_list]
    
    logger.info("Computing SHAP Values ...")
    try:
        X_trans = pipeline[:-1].transform(X)
        regressor = pipeline.named_steps["regressor"]
    except Exception:
        X_trans = X
        regressor = pipeline
        
    explainer = shap.TreeExplainer(regressor)
    shap_values = explainer(X_trans)
    shap_values.feature_names = features_list
    
    logger.info("Generating SHAP Visualization Reports ...")
    # Global Bar
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_trans, feature_names=features_list, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "08_shap_global_importance.png"))
    plt.close()
    
    # Summary Plot (Beeswarm)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_trans, feature_names=features_list, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(config.OUTPUT_DIR, "09_shap_summary_plot.png"))
    plt.close()
    
    # Planet-Level Explanation
    matches = df.index[df['planet_name'].str.contains('Proxima Cen', case=False, na=False)].tolist()
    idx_to_explain = matches[0] if matches else np.argmax(pipeline.predict(X))
    planet_name = df.loc[idx_to_explain, 'planet_name']
        
    logger.info(f"Local explanation for: {planet_name}")
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[idx_to_explain], show=False)
    plt.tight_layout()
    clean_name = "".join(c if c.isalnum() else "_" for c in planet_name)
    plt.savefig(os.path.join(config.OUTPUT_DIR, f"10_shap_waterfall_{clean_name}.png"))
    plt.close()
    
    logger.info("Exporting Feature Importance to DB ...")
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    feat_imp_df = pd.DataFrame({"feature_name": features_list, "mean_abs_shap": mean_abs_shap})
    try:
        feat_imp_df.to_sql("feature_importance_analysis", schema="exoplanet_data", con=engine, if_exists="replace", index=False)
        logger.info("Saved feature importance to DB.")
    except Exception as e:
        logger.error(f"Failed writing to DB: {e}")
        
    logger.info("Explainability Engine integration complete.")

if __name__ == "__main__":
    generate_explanations()

if __name__ == "__main__":
    generate_explanations()
