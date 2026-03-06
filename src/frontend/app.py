"""
app.py
======
Interactive Discovery Explorer and Research Interface.

Provides a unified frontend for real-time exoplanet data exploration, 
candidate prioritization, and visualization of scientific insights. 
Integrates PostgreSQL data availability with ML explainability (SHAP).
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os
import sys

# Ensure project root is in path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.config.config import config

st.set_page_config(page_title="ExoIntel AI Discovery Explorer", layout="wide")

st.title("ExoIntel – AI Discovery Explorer")

st.markdown("""
Welcome to the **ExoIntel AI Discovery Explorer**. This scientific platform analyzes exoplanets 
and automatically identifies the most promising candidates for habitability by combining robust 
machine learning predictions with analytical physical similarity metrics. 
""")

st.divider()

# --- Platform Metrics ---
def load_platform_metrics():
    engine = create_engine(config.DATABASE_URL)
    try:
        # 1. Total Planets Analyzed
        total_planets = pd.read_sql("SELECT COUNT(*) FROM exoplanet_data.planets_enriched", engine).iloc[0, 0]
        
        # 2. Total Candidates
        total_candidates = pd.read_sql("SELECT COUNT(*) FROM exoplanet_data.habitable_planet_candidates", engine).iloc[0, 0]
        
        # 3. Highest ML Score
        max_ml_score = pd.read_sql("SELECT MAX(ml_habitability_score) FROM exoplanet_data.habitable_planet_candidates", engine).iloc[0, 0]
        
        # 4. Multi-Planet Habitable Systems (score >= 0.7)
        # Checking if host_star is available, if not joining with enriched
        multi_planet_query = """
        SELECT COUNT(*) FROM (
            SELECT hpc.host_star 
            FROM exoplanet_data.habitable_planet_candidates hpc
            JOIN exoplanet_data.planets_enriched pe ON hpc.planet_name = pe.planet_name
            WHERE hpc.ml_habitability_score >= 0.7
            GROUP BY hpc.host_star
            HAVING COUNT(hpc.planet_name) > 1
        ) as sub
        """
        num_multi_systems = pd.read_sql(multi_planet_query, engine).iloc[0, 0]
        
        return {
            "total_planets": total_planets,
            "total_candidates": total_candidates,
            "max_ml_score": max_ml_score if max_ml_score else 0.0,
            "num_multi_systems": num_multi_systems
        }
    except Exception as e:
        st.error(f"Metrics load failed: {e}")
        return None

metrics = load_platform_metrics()

if metrics:
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    m_col1.metric("Planets Analyzed", f"{metrics['total_planets']:,}")
    m_col2.metric("Discovery Candidates", f"{metrics['total_candidates']:,}")
    m_col3.metric("Multi-Planet Systems", metrics["num_multi_systems"])
    m_col4.metric("Highest Habitability", f"{metrics['max_ml_score']:.3f}")

st.divider()

# --- Platform Intelligence Metrics ---
st.header("Platform Intelligence Metrics")
st.markdown("Real-time monitoring of pipeline performance, model health, and discovery yields.")

def load_intelligence_metrics():
    engine = create_engine(config.DATABASE_URL)
    intelligence = {}
    try:
        # Pipeline Performance
        intelligence["pipeline"] = pd.read_sql("SELECT timestamp, total_duration_sec, status FROM platform_metrics.pipeline_runs ORDER BY timestamp DESC LIMIT 10", engine)
        
        # Model Metrics
        intelligence["model"] = pd.read_sql("SELECT model_version, r2_score, rmse, mae, timestamp FROM platform_metrics.model_performance ORDER BY timestamp DESC LIMIT 1", engine)
        
        # Discovery Summary
        intelligence["summary"] = pd.read_sql("SELECT * FROM exoplanet_data.discovery_summary_snapshot", engine)
        
    except Exception as e:
        st.warning("Intelligence metrics not yet available. Run the autonomous pipeline to generate.")
    return intelligence

intel = load_intelligence_metrics()

if intel.get("pipeline") is not None and not intel["pipeline"].empty:
    i_col1, i_col2 = st.columns([2, 1])
    
    with i_col1:
        st.subheader("Pipeline Execution History")
        fig_duration = px.line(intel["pipeline"], x="timestamp", y="total_duration_sec", markers=True, 
                               title="Pipeline Runtime (Seconds)", labels={"total_duration_sec": "Duration (s)", "timestamp": "Execution Time"})
        st.plotly_chart(fig_duration, use_container_width=True)
        
    with i_col2:
        st.subheader("Latest Model Status")
        if not intel["model"].empty:
            m_data = intel["model"].iloc[0]
            st.metric("Model Version", m_data["model_version"])
            st.metric("R² Score", f"{m_data['r2_score']:.3f}")
            st.metric("RMSE", f"{m_data['rmse']:.4f}")
        else:
            st.info("No model performance data available.")

    st.subheader("Discovery Yield Snapshot")
    if not intel["summary"].empty:
        s_data = intel["summary"].iloc[0]
        s_col1, s_col2, s_col3, s_col4 = st.columns(4)
        s_col1.metric("Snapshot Date", datetime.fromisoformat(s_data["timestamp"]).strftime("%Y-%m-%d"))
        s_col2.metric("Avg Discovery Score", f"{s_data['average_score']:.4f}")
        s_col3.metric("Predicted Top Target", s_data["top_candidate"])
        s_col4.metric("Avg Stellar Temp", f"{s_data['avg_stellar_temp']:.1f} K")
    else:
        st.info("No discovery summary snapshot available.")
else:
    st.info("Platform intelligence data will appear here after the first automated pipeline execution.")

st.divider()

# Only load the necessary columns from the discovery table for optimized loading
def load_discovery_data():
    engine = create_engine(config.DATABASE_URL)
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

# --- Section 5: AI Research Insights ---
st.header("5. AI Research Insights")
st.markdown("This section explores visual scientific insights and machine learning explainability outputs generated continuously by the automated ExoIntel pipeline.")

st.subheader("Scientific Insights")

st.markdown("""
**Habitability vs Stellar Temperature**  
This scatter plot demonstrates the relationship between planetary habitability scores and the temperature of their host stars.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "11_habitability_vs_stellar_temp.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "11_habitability_vs_stellar_temp.png"), use_container_width=True)
else:
    st.info("Insights plot not found. Run the pipeline to generate it.")

st.markdown("""
**Habitability by Discovery Method**  
A bar chart highlighting average planetary habitability scores classified by the astronomical method used for their discovery.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "12_habitability_by_discovery_method.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "12_habitability_by_discovery_method.png"), use_container_width=True)
else:
    st.info("Insights plot not found. Run the pipeline to generate it.")

st.markdown("""
**Habitability Score Distribution**  
A histogram showing the overall distribution of ML-assigned habitability scores across the selected universe of exoplanet data.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "13_habitability_score_distribution.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "13_habitability_score_distribution.png"), use_container_width=True)
else:
    st.info("Insights plot not found. Run the pipeline to generate it.")

st.markdown("""
**Insight Correlation Heatmap**  
A correlation heatmap visualizing underlying statistical relationships between various planetary constraints and stellar metrics.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "14_insight_correlation_heatmap.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "14_insight_correlation_heatmap.png"), use_container_width=True)
else:
    st.info("Insights plot not found. Run the pipeline to generate it.")

st.divider()

st.subheader("Model Explainability (SHAP)")

st.markdown("""
**Global SHAP Feature Importance**  
Identifies the most significant astrophysical features driving the machine learning model's predictive habitability decisions globally.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "08_shap_global_importance.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "08_shap_global_importance.png"), use_container_width=True)
else:
    st.info("Explainability plot not found. Run the pipeline to generate it.")

st.markdown("""
**SHAP Summary Plot**  
Visualizes the aggregate distribution of SHAP impact values for features, demonstrating how feature variations shift predictions positively or negatively.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "09_shap_summary_plot.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "09_shap_summary_plot.png"), use_container_width=True)
else:
    st.info("Explainability plot not found. Run the pipeline to generate it.")

st.markdown("""
**Planet Explanation Waterfall Plot (Proxima Cen b)**  
A deeply localized explainability waterfall showing how individual astronomical features sequentially accumulated to determine the final machine learning score for Proxima Cen b.
""")
if os.path.exists(os.path.join(config.OUTPUT_DIR, "10_shap_waterfall_Proxima_Cen_b.png")):
    st.image(os.path.join(config.OUTPUT_DIR, "10_shap_waterfall_Proxima_Cen_b.png"), use_container_width=True)
else:
    st.info("Explainability plot not found. Run the pipeline to generate it.")
