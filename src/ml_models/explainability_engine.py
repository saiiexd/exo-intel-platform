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

def generate_explanations():
    print("=" * 65)
    print("  ExoIntel – Phase 5: XAI for Habitability Predictions")
    print("=" * 65)
    
    engine = get_engine()
    
    print("\n[1/5] Loading Enriched Dataset ...")
    df = pd.read_sql("SELECT * FROM exoplanet_data.planets_enriched", engine)
    
    # Needs matching feature structure
    if not os.path.exists(MODEL_PATH):
        print(f"Error: Model not found at {MODEL_PATH}")
        return
        
    print("\n[2/5] Loading the Trained ML Model ...")
    artifact = joblib.load(MODEL_PATH)
    pipeline = artifact.get("pipeline", artifact)
    features_list = artifact.get("features", None)
    
    if not features_list:
        features_list = [
            "planet_radius", "planet_mass", "planet_density",
            "equilibrium_temperature", "stellar_temperature",
            "stellar_mass", "stellar_radius"
        ]
        
    df = df.dropna(subset=features_list).copy()
    df.reset_index(drop=True, inplace=True)
    X = df[features_list]
    
    print("\n[3/5] Computing SHAP Values (TreeExplainer) ...")
    # Apply preprocessing steps to get input for the model
    try:
        X_trans = pipeline[:-1].transform(X)
        regressor = pipeline.named_steps["regressor"]
    except Exception as e:
        print("Pipeline parsing error, using as is.", e)
        X_trans = X
        regressor = pipeline
        
    explainer = shap.TreeExplainer(regressor)
    shap_values = explainer(X_trans)
    
    # Assign actual feature names mapping
    shap_values.feature_names = features_list
    
    print("\n[4/5] Generating SHAP Visualization Reports ...")
    # 1. Global Bar
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_trans, feature_names=features_list, plot_type="bar", show=False)
    plt.title("Global Feature Importance (SHAP Mean Absolute Value)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "08_shap_global_importance.png"))
    plt.close()
    
    # 2. Summary Plot (Beeswarm)
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values, X_trans, feature_names=features_list, show=False)
    plt.title("SHAP Summary Plot (Feature Impacts)")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "09_shap_summary_plot.png"))
    plt.close()
    plt.clf()
    
    # 3. Planet-Level Explanation (Waterfall)
    # Search for a good candidate, e.g., Proxima Cen b
    idx_to_explain = 0
    matches = df.index[df['planet_name'].str.contains('Proxima Cen', case=False, na=False)].tolist()
    if matches:
        idx_to_explain = matches[0]
        planet_name = df.loc[idx_to_explain, 'planet_name']
    else:
        # Fallback to the one with highest prediction
        preds = pipeline.predict(X)
        idx_to_explain = np.argmax(preds)
        planet_name = df.loc[idx_to_explain, 'planet_name']
        
    print(f"      Selected example for local explanation: {planet_name}")
    
    # Waterfall
    plt.figure(figsize=(10, 6))
    shap.plots.waterfall(shap_values[idx_to_explain], show=False)
    plt.title(f"SHAP Local Explanation for {planet_name}")
    plt.tight_layout()
    # Save with a clean name
    clean_name = "".join(c if c.isalnum() else "_" for c in planet_name)
    plt.savefig(os.path.join(OUT_DIR, f"10_shap_waterfall_{clean_name}.png"))
    plt.close()
    
    print("\n[5/5] Exporting Feature Importance to DB ...")
    # Compute mean absolute SHAP for each feature
    mean_abs_shap = np.abs(shap_values.values).mean(axis=0)
    feat_imp_df = pd.DataFrame({
        "feature_name": features_list,
        "mean_abs_shap": mean_abs_shap
    }).sort_values(by="mean_abs_shap", ascending=False)
    
    try:
        feat_imp_df.to_sql(
            "feature_importance_analysis",
            schema="exoplanet_data",
            con=engine,
            if_exists="replace",
            index=False
        )
        print("      Saved feature importance summary to 'exoplanet_data.feature_importance_analysis'.")
    except Exception as e:
        print(f"      Failed writing to database: {e}")
        
    print("\n✅ Phase 5 Complete. XAI Engine integration finished.")
    print("=" * 65)

if __name__ == "__main__":
    generate_explanations()
