import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
import numpy as np

engine = create_engine(
    "postgresql://postgres:saivenkat143@localhost/exo_intel_db"
)

query = """
SELECT
planet_radius,
planet_mass,
planet_density,
equilibrium_temperature,
stellar_temperature,
stellar_mass,
stellar_radius,
habitability_index
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

X = df[features]
y = df["habitability_index"]

model = RandomForestRegressor(
n_estimators=200,
max_depth=10,
random_state=42
)

scores = cross_val_score(
model,
X,
y,
cv=5,
scoring="r2"
)

print("\nCross Validation R2 Scores:")
print(scores)

print("\nMean R2:", np.mean(scores))
print("Std Dev:", np.std(scores))