import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:saivenkat143@localhost/exo_intel_db"
)

model = joblib.load("src/ml_models/habitability_model.pkl")

query = """
SELECT
rule_based_score,
ml_score
FROM exoplanet_data.habitability_model_results
"""

df = pd.read_sql(query, engine)

features = [
"planet_radius",
"planet_mass",
"planet_density",
"equilibrium_temperature",
"stellar_temperature",
"stellar_mass",
"stellar_radius"
]

importances = model.feature_importances_

importance_df = pd.DataFrame({
"feature": features,
"importance": importances
}).sort_values(by="importance", ascending=True)

plt.figure()
plt.barh(importance_df["feature"], importance_df["importance"])
plt.title("Feature Importance for Habitability Prediction")
plt.xlabel("Importance")
plt.ylabel("Feature")
plt.tight_layout()
plt.savefig("data/processed/feature_importance_plot.png")

plt.figure()
plt.scatter(df["rule_based_score"], df["ml_score"])
plt.title("Rule-Based vs ML Predicted Habitability")
plt.xlabel("Rule-Based Habitability Score")
plt.ylabel("ML Predicted Habitability Score")
plt.tight_layout()
plt.savefig("data/processed/model_comparison_scatter.png")

print("Plots saved in data/processed/")