from fastapi import FastAPI
import joblib
import pandas as pd

app = FastAPI()

model = joblib.load("models/habitability_model_v1.pkl")


@app.get("/")
def home():
    return {"message": "ExoIntel Habitability Prediction API"}


@app.post("/predict")
def predict_habitability(
    planet_radius: float,
    planet_mass: float,
    planet_density: float,
    equilibrium_temperature: float,
    stellar_temperature: float,
    stellar_mass: float,
    stellar_radius: float,
    earth_similarity_score: float
):

    data = pd.DataFrame([{
        "planet_radius": planet_radius,
        "planet_mass": planet_mass,
        "planet_density": planet_density,
        "equilibrium_temperature": equilibrium_temperature,
        "stellar_temperature": stellar_temperature,
        "stellar_mass": stellar_mass,
        "stellar_radius": stellar_radius,
        "earth_similarity_score": earth_similarity_score
    }])

    prediction = model.predict(data)[0]

    if prediction == 1:
        result = "Potentially Habitable"
    else:
        result = "Not Habitable"

    return {"prediction": result}