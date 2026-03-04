import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
import joblib

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

X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(
n_estimators=200,
max_depth=10,
random_state=42
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("R2 Score:", r2_score(y_test, predictions))
print("RMSE:", mean_squared_error(y_test, predictions) ** 0.5)

joblib.dump(model, "src/ml_models/habitability_model.pkl")

print("Model saved successfully")