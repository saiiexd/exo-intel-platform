import joblib
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:saivenkat143@localhost/exo_intel_db"
)

model = joblib.load("src/ml_models/habitability_model.pkl")

query = """
SELECT
planet_radius,
planet_mass,
planet_density,
equilibrium_temperature,
stellar_temperature,
stellar_mass,
stellar_radius
FROM exoplanet_data.planets
WHERE habitability_index IS NOT NULL
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
}).sort_values(by="importance", ascending=False)

print("\nFeature Importance:\n")
print(importance_df)

importance_df.to_csv(
"data/processed/feature_importance.csv",
index=False
)

print("\nFeature importance saved to data/processed/feature_importance.csv")