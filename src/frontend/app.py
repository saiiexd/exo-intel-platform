import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import joblib
import numpy as np
import os

st.set_page_config(page_title="ExoIntel AI Discovery Explorer", layout="wide")

st.title("ExoIntel – AI Discovery Explorer")

st.markdown("""
Welcome to the **ExoIntel AI Discovery Explorer**. This scientific platform analyzes exoplanets 
and automatically identifies the most promising candidates for habitability by combining robust 
machine learning predictions with analytical physical similarity metrics. 
""")

st.divider()

# Only load the necessary columns from the discovery table for optimized loading
@st.cache_data
def load_discovery_data():
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
        stellar_radius,
        earth_similarity_approx as earth_similarity_score,
        stellar_habitability_factor,
        ml_habitability_score,
        combined_discovery_score as discovery_score,
        discovery_rank
    FROM exoplanet_data.habitable_planet_candidates
    ORDER BY discovery_rank ASC
    """
    return pd.read_sql(query, engine)

try:
    df_candidates = load_discovery_data()
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

# --- Section 1: AI Discovery Leaderboard ---
st.header("1. AI Discovery Leaderboard")
st.markdown("Top 20 candidates ranked by the composite Discovery Score.")

top_20 = df_candidates.head(20).copy()

# Format for display
display_top_20 = top_20[["discovery_rank", "planet_name", "discovery_score", "ml_habitability_score", "earth_similarity_score"]].copy()
display_top_20.columns = ["Rank", "Planet Name", "Discovery Score", "ML Score", "Earth Similarity Score"]

st.dataframe(display_top_20, hide_index=True, use_container_width=True)

st.divider()

# --- Section 2: Habitability Explorer ---
st.header("2. Habitability Explorer")
st.markdown("Interactively filter the planetary candidates using dynamic thresholds.")

col1, col2 = st.columns(2)
min_ml = col1.slider("Minimum ML Habitability Score", 0.0, 1.0, 0.5, 0.01)
min_ess = col2.slider("Minimum Earth Similarity Score", 0.0, 1.0, 0.5, 0.01)

filtered_df = df_candidates[
    (df_candidates["ml_habitability_score"] >= min_ml) &
    (df_candidates["earth_similarity_score"] >= min_ess)
]

st.metric("Total Candidates Matching Criteria", len(filtered_df))
st.dataframe(filtered_df, hide_index=True, use_container_width=True)

st.divider()

# --- Section 3: Physical Similarity vs ML Predictions ---
st.header("3. Physical Similarity vs ML Predictions")
st.markdown("This scatter plot visualizes the consensus between the analytical Earth Similarity Score and the Machine Learning Habitability Score.")

if not filtered_df.empty:
    fig_scatter = px.scatter(
        filtered_df,
        x="earth_similarity_score",
        y="ml_habitability_score",
        size="discovery_score",
        hover_name="planet_name",
        color="stellar_habitability_factor",
        color_continuous_scale="viridis",
        size_max=40,
        title="ML Habitability vs Earth Similarity (Bubble Size = Discovery Score)",
        labels={
            "earth_similarity_score": "Earth Similarity Score",
            "ml_habitability_score": "ML Habitability Score",
            "stellar_habitability_factor": "Stellar Habitability Factor"
        }
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.warning("No planets match the active filters to display the scatter plot.")

st.divider()

# --- Section 4: Planet Detail Viewer ---
st.header("4. Planet Detail Viewer")
st.markdown("Select a planet to deeply inspect its astrophysical parameters and associated scores.")

selected_planet = st.selectbox("Select Planet:", df_candidates["planet_name"].sort_values())
planet_details = df_candidates[df_candidates["planet_name"] == selected_planet].iloc[0]

colA, colB, colC, colD = st.columns(4)
colA.metric("Discovery Rank", f"#{int(planet_details['discovery_rank'])}")
colB.metric("Discovery Score", round(planet_details["discovery_score"], 3))
colC.metric("ML Habitability Score", round(planet_details["ml_habitability_score"], 3))
colD.metric("Earth Similarity Score", round(planet_details["earth_similarity_score"], 3))

st.subheader("Physical Parameters")
colE, colF, colG, colH = st.columns(4)
colE.metric("Planet Radius (Earth=1)", round(planet_details["planet_radius"], 2))
colF.metric("Planet Mass (Earth=1)", round(planet_details["planet_mass"], 2))
colG.metric("Planet Density", round(planet_details["planet_density"], 2))
colH.metric("Equilibrium Temp (K)", round(planet_details["equilibrium_temperature"], 2))

st.subheader("Stellar Parameters")
colI, colJ, colK, colL = st.columns(4)
colI.metric("Stellar Temperature (K)", round(planet_details["stellar_temperature"], 2))
colJ.metric("Stellar Mass (Sun=1)", round(planet_details["stellar_mass"], 2))
colK.metric("Stellar Radius (Sun=1)", round(planet_details["stellar_radius"], 2))
colL.metric("Stellar Habitability Factor", round(planet_details["stellar_habitability_factor"], 3))

st.divider()

# --- Section 5: Habitability Prediction Simulator (Legacy) ---
st.header("5. Hypothetical Planet Simulator")
st.markdown("""
Use the sliders below to simulate a completely hypothetical planet and evaluate its potential habitability 
using our trained machine learning model.
""")

col1_sim, col2_sim = st.columns(2)

planet_radius_sim = col1_sim.slider("Planet Radius (Earth Radii)", 0.1, 20.0, 1.0)
planet_mass_sim = col2_sim.slider("Planet Mass (Earth Mass)", 0.1, 50.0, 1.0)

planet_density_sim = col1_sim.slider("Planet Density", 0.1, 20.0, 5.5)
equilibrium_temperature_sim = col2_sim.slider("Equilibrium Temperature (Kelvin)", 50.0, 2000.0, 288.0)

stellar_temperature_sim = col1_sim.slider("Host Star Temperature (Kelvin)", 2000.0, 10000.0, 5500.0)
stellar_mass_sim = col2_sim.slider("Host Star Mass (Solar Mass)", 0.1, 5.0, 1.0)

stellar_radius_sim = st.slider("Host Star Radius (Solar Radius)", 0.1, 10.0, 1.0)

predict_button = st.button("Predict Habitability for Hypothetical Planet")

# Handle model loading centrally
model_path = "src/ml_models/habitability_model.pkl"
model = None
features_list = [
    "planet_radius", "planet_mass", "planet_density",
    "equilibrium_temperature", "stellar_temperature",
    "stellar_mass", "stellar_radius"
]

if os.path.exists(model_path):
    artifact = joblib.load(model_path)
    model = artifact.get("pipeline", artifact) # Handle both dict and raw pipeline
    features_list = artifact.get("features", features_list)

if predict_button:
    if model is not None:
        input_data = {
            "planet_radius": planet_radius_sim,
            "planet_mass": planet_mass_sim,
            "planet_density": planet_density_sim,
            "equilibrium_temperature": equilibrium_temperature_sim,
            "stellar_temperature": stellar_temperature_sim,
            "stellar_mass": stellar_mass_sim,
            "stellar_radius": stellar_radius_sim
        }
        input_df = pd.DataFrame([input_data])[features_list]

        raw_prediction = model.predict(input_df)[0]
        prediction = float(raw_prediction)
        
        with st.expander("🔍 Predictor Debug Info"):
            st.write("Constructed Input DataFrame:")
            st.dataframe(input_df)
            st.write(f"Raw Model Prediction: {raw_prediction}")
            st.write(f"Clamped Prediction: {max(0.0, min(1.0, prediction))}")

        prediction = max(0.0, min(1.0, prediction))

        st.subheader("Prediction Result")
        st.metric("Predicted Habitability Score", round(prediction, 3))

        if prediction > 0.8:
            st.success("This simulated planet shows strong potential for habitability based on model predictions.")
        elif prediction > 0.5:
            st.warning("This planet may have moderate habitability potential.")
        else:
            st.error("This planet is unlikely to support Earth-like conditions.")
