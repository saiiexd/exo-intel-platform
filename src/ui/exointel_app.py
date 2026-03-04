import streamlit as st
import joblib
import pandas as pd

st.title("ExoIntel: Exoplanet Habitability Analyzer")

st.write("Enter planetary parameters to predict potential habitability.")

model = joblib.load("models/habitability_model_v1.pkl")


planet_radius = st.number_input("Planet Radius (Earth radii)", value=1.0)
planet_mass = st.number_input("Planet Mass (Earth masses)", value=1.0)
planet_density = st.number_input("Planet Density", value=1.0)
equilibrium_temperature = st.number_input("Equilibrium Temperature (K)", value=288.0)

stellar_temperature = st.number_input("Stellar Temperature (K)", value=5778.0)
stellar_mass = st.number_input("Stellar Mass (Solar masses)", value=1.0)
stellar_radius = st.number_input("Stellar Radius (Solar radii)", value=1.0)

earth_similarity_score = st.number_input("Earth Similarity Score", value=0.8)


if st.button("Predict Habitability"):

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
        st.success("Potentially Habitable Planet")
    else:
        st.error("Not Habitable")