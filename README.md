# ExoIntel: AI Exoplanet Discovery Platform 🪐

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Machine Learning](https://img.shields.io/badge/ML-Gradient_Boosting-F7931E?style=flat)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**ExoIntel** is a high-performance, end-to-end data intelligence system designed to automate the discovery and analysis of habitable exoplanets. By fusing astronomical data engineering with advanced machine learning, explainable AI (XAI), and interactive dashboards, ExoIntel transforms raw stellar observations into prioritized scientific insights.

---

## ⚡ Quick Demo

Rebuild the entire universe and launch the explorer in two simple steps:

1. **Orchestrate the Pipeline**: Run the full automated cycle (Data Cleaning → ML Training → Discovery → XAI → Insights).
   ```bash
   python run_exointel_pipeline.py
   ```

2. **Explore Research Insights**: Launch the interactive AI Research Dashboard.
   ```bash
   streamlit run src/frontend/app.py
   ```

---

## ✨ Project Highlights

- **🎯 AI-Based Habitability Prediction**: Utilizes a Gradient Boosting Regressor to compute a high-precision Habitability Index for thousands of exoplanets based on planetary and stellar physics.
- **🏆 Automated Discovery Ranking**: Intelligent ranking subsystem that prioritizes candidates by combining ML scores with Earth Similarity indices and stellar habitat factors.
- **🔍 Explainable AI (SHAP)**: Transcends "black-box" ML by using SHAP values to visualize exactly how planetary mass, radius, and temperature influenced every single prediction.
- **📊 Scientific Insight Analytics**: Automated generation of publication-ready visualizations, including habitability distributions, correlation heatmaps, and stellar trend analyses.
- **🛰️ Interactive Research Interface**: A Streamlit-powered frontend for deep-diving into individual planets and simulating hypothetical planetary scenarios.

---

## ⚙️ System Workflow

The platform follows a modular, linear-flow architecture:

1. **Ingestion & Data Warehouse**: Raw astronomical data is stored in **PostgreSQL**.
2. **Feature Engineering**: `dataset_analysis.py` cleans data and derives physical similarity metrics.
3. **ML Pipeline**: `train_habitability_model.py` trains and optimizes the habitability model.
4. **Discovery Engine**: `planet_discovery_engine.py` performs batch predictions across the entire catalog.
5. **Explainability Layer**: `explainability_engine.py` computes SHAP values for global and local transparency.
6. **Insight Generation**: `insight_engine.py` produces complex statistical charts and research tables.
7. **Interactive Dashboard**: `app.py` presents findings through an immersive UI.

---

## 🛠️ Technology Stack

- **Languages**: Python (Core Logic)
- **Database**: PostgreSQL (Data Warehouse), SQLAlchemy (ORM)
- **Machine Learning**: Scikit-Learn (Gradient Boosting), NumPy, Pandas
- **Explainability**: SHAP (Shapley Additive Explanations)
- **Frontend/Viz**: Streamlit, Plotly, Matplotlib, Seaborn
- **Automation**: Subprocess-based Orchestration

---

## 🖼️ Demo & Visualizations

The ExoIntel pipeline automatically generates these insights to help researchers interpret planetary trends:

### 1. Global Feature Importance (XAI)
![SHAP Global Importance](analysis_outputs/08_shap_global_importance.png)
*This chart identifies which astrophysical features (like Planetary Equilibrium Temp and Radius) drive the model's habitability predictions globally.*

### 2. Habitability vs. Stellar Temperature
![Habitability Trends](analysis_outputs/11_habitability_vs_stellar_temp.png)
*A scientific scatter plot demonstrating the "Goldilocks" distribution of habitable candidates relative to their host star's temperature.*

### 3. SHAP Summary Distribution
![SHAP Summary](analysis_outputs/09_shap_summary_plot.png)
*Visualizes how variations in specific features (e.g., higher stellar mass vs lower temperature) shift the final habitability score.*

### 4. Insight Correlation Heatmap
![Correlation Heatmap](analysis_outputs/14_insight_correlation_heatmap.png)
*A statistical overview revealing hidden relationships between planetary constraints and system-wide habitability factors.*

---

## 📂 Repository Structure

- `src/data_analysis/`: Data cleaning, enrichment, and feature engineering logic.
- `src/ml_models/`: ML training scripts, model artifacts, and **SHAP explainability** engine.
- `src/discovery/`: Ranking algorithms and batch prediction system.
- `src/analytics/`: The **Insight Engine** for automated research visualization.
- `src/frontend/`: Source code for the **Streamlit** AI Discovery Explorer.
- `analysis_outputs/`: Directory containing dynamically updated research plots and analytics.
- `docs/`: Technical documentation including system architecture diagrams.
- `pipeline_logs/`: Performance reports and execution logs for the automated orchestrator.

---

## 🚀 Getting Started

### 1. Installation
Clone the repository and install the scientific stack:
```bash
git clone https://github.com/yourusername/exo-intel-platform.git
cd exo-intel-platform
pip install -r requirements.txt
```

### 2. Database Configuration
Ensure PostgreSQL is running and update your connection string in `src/utils/db.py`:
```python
# Example URI
DATABASE_URL = "postgresql://postgres:password@localhost:5432/exo_intel_db"
```

### 3. Execute the Autonomous Pipeline
Run everything from data ingestion to scientific insights with one command:
```bash
python run_exointel_pipeline.py
```

### 4. Launch the Research Dashboard
```bash
streamlit run src/frontend/app.py
```

---

## 🐳 Deployment & Running with Docker

ExoIntel is fully containerized for production-ready deployment.

### 1. Configure Environment
Copy the example environment file and update your database credentials:
```bash
cp .env.example .env
```

### 2. Launch with Docker Compose
One command to spin up both the **Postgres Database** and the **Streamlit Application**:
```bash
docker-compose up --build
```
- **Streamlit UI**: `http://localhost:8501`
- **Postgres DB**: `localhost:5432`

---

## ⚙️ Configuration & Production Readiness

The platform uses a centralized configuration system (`src/config/config.py`) that manages:
- **Environment Variables**: All sensitive DB credentials and server ports are loaded via `.env`.
- **System Health Checks**: `src/utils/system_health_check.py` automatically verifies DB connectivity, table schemas, and model artifacts before the pipeline runs.
- **Structured Logging**: Detailed logs are written to `pipeline_logs/` using a standardized logger, enabling easy production monitoring.

---

## 🔄 Updating the Repository

To maintain the project's portfolio quality and stay synchronized with GitHub, use the automated sync utility:

### 1. Synchronize to GitHub
Stage, commit, and push all recent changes (including code, documentation, and analysis plots) with a single command:
```bash
# Automated sync with timestamped message
python github_sync.py

# Manual sync with custom message
python github_sync.py -m "Integrated new SHAP waterfall plots"
```

### 2. Version Tagging
Mark major milestones with semantic version tags (e.g., `v1.0.0`):
```bash
python github_sync.py -t v1.1.0
```
This will automatically create a local tag and push it to the GitHub repository.

---

## 👤 Author
**Sai Venkat**  
*Data Scientist & Space Research Enthusiast*

---
*Disclaimer: Habitability scores are generated by machine learning models based on current astronomical datasets and are intended for research demonstration purposes.*
