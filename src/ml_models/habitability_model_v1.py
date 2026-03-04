import psycopg2
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


# DATABASE CONNECTION
conn = psycopg2.connect(
    host="localhost",
    database="exo_intel_db",
    user="postgres",
    password="saivenkat143"
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
earth_similarity_score,
habitable_zone
FROM exoplanet_data.planets
WHERE earth_similarity_score IS NOT NULL
"""

df = pd.read_sql(query, conn)
conn.close()


# CONVERT LABEL INTO BINARY TARGET
df["target"] = df["habitable_zone"].apply(
    lambda x: 1 if x == "potential_habitable" else 0
)


# FEATURES AND TARGET
X = df[
    [
        "planet_radius",
        "planet_mass",
        "planet_density",
        "equilibrium_temperature",
        "stellar_temperature",
        "stellar_mass",
        "stellar_radius",
        "earth_similarity_score"
    ]
]

y = df["target"]


# TRAIN TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# MODEL
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)


# PREDICTIONS
predictions = model.predict(X_test)


print("Model Evaluation")
print(classification_report(y_test, predictions))

import joblib

joblib.dump(model, "models/habitability_model_v1.pkl")

print("Model saved")

# FEATURE IMPORTANCE

import pandas as pd

feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
})

feature_importance = feature_importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance Ranking")
print(feature_importance)

feature_importance.to_csv("models/feature_importance_v1.csv", index=False)