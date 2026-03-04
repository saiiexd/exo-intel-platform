import pandas as pd
import joblib
import numpy as np
from sqlalchemy import create_engine, text

# DATABASE CONNECTION
engine = create_engine(
    "postgresql://postgres:saivenkat143@localhost/exo_intel_db"
)

# LOAD TRAINED MODEL
model = joblib.load("src/ml_models/habitability_model.pkl")

# LOAD PLANET DATA
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

# FEATURES USED BY MODEL
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

# GET PREDICTIONS FROM EACH TREE
tree_predictions = np.array([tree.predict(X) for tree in model.estimators_])

# FINAL ML SCORE
df["ml_score"] = tree_predictions.mean(axis=0)

# UNCERTAINTY
df["prediction_uncertainty"] = tree_predictions.std(axis=0)

# CONFIDENCE SCORE
df["confidence_score"] = 1 / (1 + df["prediction_uncertainty"])

# KEEP ONLY REQUIRED COLUMNS
prediction_df = df[
[
"planet_id",
"ml_score",
"prediction_uncertainty",
"confidence_score"
]
]

# CLEAR OLD DATA (DO NOT DROP TABLE)
with engine.connect() as conn:
    conn.execute(text("DELETE FROM exoplanet_data.ml_habitability_predictions"))

# INSERT NEW DATA
prediction_df.to_sql(
name="ml_habitability_predictions",
con=engine,
schema="exoplanet_data",
if_exists="append",
index=False
)

print("Habitability predictions updated successfully.")