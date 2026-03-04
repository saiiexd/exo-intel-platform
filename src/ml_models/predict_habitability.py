import pandas as pd
import joblib
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:saivenkat143@localhost/exo_intel_db"
)

model = joblib.load("src/ml_models/habitability_model.pkl")

query = """
SELECT
planet_id,
planet_radius,
planet_mass,
planet_density,
equilibrium_temperature,
stellar_temperature,
stellar_mass,
stellar_radius
FROM exoplanet_data.planets
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

X = df[features]

df["ml_predicted_habitability"] = model.predict(X)

df[["planet_id","ml_predicted_habitability"]].to_sql(
"ml_habitability_predictions",
engine,
schema="exoplanet_data",
if_exists="replace",
index=False
)

print("Predictions stored in database")