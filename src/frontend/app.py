import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import joblib
import numpy as np
import os

st.set_page_config(page_title="ExoIntel Planet Habitability Intelligence System", layout="wide")

st.title("ExoIntel – AI System for Exoplanet Habitability Analysis")

st.markdown("""
This platform analyzes exoplanet characteristics and estimates the **habitability potential** of planets using a machine learning model.

The model evaluates astrophysical properties such as:

• Planet radius  
• Planet mass  
• Planet density  
• Planet temperature  
• Host star temperature  
• Host star mass  
• Host star radius  

The system was trained using known exoplanet datasets to identify patterns that correlate with Earth-like conditions.

Habitability scores closer to **1** indicate higher similarity to Earth-like environments.
""")

engine = create_engine("postgresql://postgres:saivenkat143@localhost:5432/exo_intel_db")

query = """
SELECT
planet_name,
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

df = df.fillna(0)

st.divider()

st.header("Dataset Overview")

col1,col2,col3,col4 = st.columns(4)

col1.metric("Total Planets",len(df))
col2.metric("Average Radius",round(df["planet_radius"].mean(),2))
col3.metric("Average Mass",round(df["planet_mass"].mean(),2))
col4.metric("Average Temperature",round(df["equilibrium_temperature"].mean(),2))

st.markdown("""
The dataset contains thousands of confirmed exoplanets discovered by different astronomical techniques.
These planets orbit stars across our galaxy and vary widely in their physical properties.

Understanding these parameters helps scientists estimate which planets could potentially support life.
""")

st.divider()

st.header("Planet Distribution Analysis")

colA,colB = st.columns(2)

fig1 = px.histogram(
df,
x="planet_radius",
nbins=40,
title="Distribution of Planet Radius"
)

colA.plotly_chart(fig1,width="stretch")

fig2 = px.histogram(
df,
x="planet_mass",
nbins=40,
title="Distribution of Planet Mass"
)

colB.plotly_chart(fig2,width="stretch")

colC,colD = st.columns(2)

fig3 = px.scatter(
df,
x="equilibrium_temperature",
y="planet_radius",
size="planet_mass",
hover_name="planet_name",
title="Planet Temperature vs Radius"
)

colC.plotly_chart(fig3,width="stretch")

fig4 = px.scatter(
df,
x="stellar_temperature",
y="planet_mass",
size="planet_radius",
hover_name="planet_name",
title="Star Temperature vs Planet Mass"
)

colD.plotly_chart(fig4,width="stretch")

st.markdown("""
These plots show the diversity of planetary systems discovered so far.

Large planets tend to dominate discovery datasets because they are easier to detect using transit and radial velocity methods.

Smaller Earth-sized planets are harder to detect but are the most interesting from a habitability perspective.
""")

st.divider()

st.header("Planet Explorer")

planet = st.selectbox("Select a planet to inspect its parameters",df["planet_name"])

selected = df[df["planet_name"]==planet]

st.dataframe(selected,width="stretch")

st.markdown("""
This explorer allows inspection of the physical parameters for each known exoplanet in the dataset.
""")

st.divider()

st.header("Habitability Prediction Simulator")

st.markdown("""
Use the sliders below to simulate a hypothetical planet and evaluate its potential habitability.

Adjust planetary and stellar parameters, then click **Predict Habitability** to evaluate the planet.
""")

col1,col2 = st.columns(2)

planet_radius = col1.slider("Planet Radius (Earth Radii)",0.1,20.0,1.0)
planet_mass = col2.slider("Planet Mass (Earth Mass)",0.1,50.0,1.0)

planet_density = col1.slider("Planet Density",0.1,20.0,5.5)
equilibrium_temperature = col2.slider("Equilibrium Temperature (Kelvin)",50,2000,288)

stellar_temperature = col1.slider("Host Star Temperature (Kelvin)",2000,10000,5500)
stellar_mass = col2.slider("Host Star Mass (Solar Mass)",0.1,5.0,1.0)

stellar_radius = st.slider("Host Star Radius (Solar Radius)",0.1,10.0,1.0)

predict_button = st.button("Predict Habitability")

model_path = "src/ml_models/habitability_model.pkl"

if predict_button:

    if os.path.exists(model_path):

        model = joblib.load(model_path)

        features = np.array([[planet_radius,
                              planet_mass,
                              planet_density,
                              equilibrium_temperature,
                              stellar_temperature,
                              stellar_mass,
                              stellar_radius]])

        prediction = model.predict(features)[0]

        st.subheader("Prediction Result")

        st.metric("Predicted Habitability Score",round(prediction,3))

        if prediction > 0.8:

            st.success("This simulated planet shows strong potential for habitability based on model predictions.")

        elif prediction > 0.5:

            st.warning("This planet may have moderate habitability potential.")

        else:

            st.error("This planet is unlikely to support Earth-like conditions.")

        st.markdown("""
Interpretation of Habitability Score:

• **0.8 – 1.0** : Highly Earth-like conditions  
• **0.5 – 0.8** : Potentially habitable environment  
• **0.2 – 0.5** : Unlikely but possible under special conditions  
• **0.0 – 0.2** : Extremely low habitability likelihood
""")

st.divider()

st.header("Machine Learning Model Explanation")

st.markdown("""
The prediction model is a **Random Forest Regression model**.

Random Forest works by building many decision trees that analyze different combinations of planetary and stellar properties.

Each tree predicts a habitability score, and the final output is the average prediction from all trees.

This approach helps capture complex nonlinear relationships between astrophysical variables.
""")

model = joblib.load(model_path)

if hasattr(model,"feature_importances_"):

    importance = model.feature_importances_

    features = [
    "planet_radius",
    "planet_mass",
    "planet_density",
    "equilibrium_temperature",
    "stellar_temperature",
    "stellar_mass",
    "stellar_radius"
    ]

    imp_df = pd.DataFrame({
    "feature":features,
    "importance":importance
    })

    fig5 = px.bar(
    imp_df,
    x="feature",
    y="importance",
    title="Feature Importance in Habitability Prediction"
    )

    st.plotly_chart(fig5,width="stretch")

st.markdown("""
Feature importance shows which astrophysical parameters influence habitability predictions the most.

Planet radius and temperature typically play a strong role because they determine whether a planet could maintain liquid water and a stable atmosphere.
""")

st.divider()

st.header("Scientific Context")

st.markdown("""
Habitability prediction is one of the central challenges of modern astrophysics.

Astronomers search for planets within the **habitable zone**, a region around a star where temperatures could allow liquid water to exist.

However, true habitability depends on many additional factors:

• Atmospheric composition  
• Magnetic field protection  
• Geological activity  
• Stellar radiation environment  

Machine learning models like this one help researchers analyze large datasets of planetary systems and identify promising candidates for further observation.
""")