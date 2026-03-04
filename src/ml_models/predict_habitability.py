import joblib
import pandas as pd

# load trained model
model = joblib.load("models/habitability_model_v1.pkl")

print("Model loaded")

# example planet input
data = {
    "planet_radius": [1.2],
    "planet_mass": [1.5],
    "planet_density": [0.87],
    "equilibrium_temperature": [290],
    "stellar_temperature": [5700],
    "stellar_mass": [1.0],
    "stellar_radius": [1.0],
    "earth_similarity_score": [0.82]
}

planet = pd.DataFrame(data)

prediction = model.predict(planet)

if prediction[0] == 1:
    print("Prediction: Potentially Habitable Planet")
else:
    print("Prediction: Not Habitable")