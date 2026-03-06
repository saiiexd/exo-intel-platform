# ExoIntel AI Exoplanet Discovery Platform

ExoIntel is an advanced, production-grade AI platform designed for the automated discovery and scientific analysis of potentially habitable exoplanets. By integrating high-fidelity astronomical data engineering with Gradient Boosting machine learning models and SHAP-based explainability, ExoIntel provides a comprehensive research framework for identifying high-priority planetary candidates.

## Key Capabilities

*   **Machine Learning Prediction**: High-precision habitability indexing using Gradient Boosting regression models.
*   **Discovery Ranking Subsystem**: Weighted prioritization engine combining ML scores with Earth Similarity analytical indices.
*   **Explainable AI (XAI)**: Full model transparency via SHAP (Shapley Additive Explanations) for both global and local feature analysis.
*   **Scientific Insight Analytics**: Automated generation of publication-quality statistical visualizations and astrophysical trend reports.
*   **End-to-End Orchestration**: A robust, single-command pipeline for data cleansing, model training, and insight generation.

## System Architecture

ExoIntel follows a modular, pipeline-oriented architecture designed for scalability and scientific reproducibility.

1.  **Data Warehouse Layer**: Persistent storage of astronomical observations in a PostgreSQL database.
2.  **Engineering Layer**: Automated data cleansing, outlier detection, and astrophysical feature derivation.
3.  **Modeling Layer**: Supervised learning pipeline for habitability prediction and model persistence.
4.  **Inference & Ranking Layer**: Batch processing of planetary catalogs to generate a prioritized discovery standing.
5.  **Analytics Layer**: Statistical Insight Engine and XAI Interpreter for scientific validation.
6.  **Presentation Layer**: High-performance interactive dashboard for research exploration.

## Pipeline Workflow

The ExoIntel platform orchestrates data flow through the following integrated sequence:

1.  **Dataset Analysis**: `src/data_analysis/dataset_analysis.py` - Performs outlier removal (Z-score/IQR) and engineers Earth Similarity indices.
2.  **Model Training**: `src/ml_models/train_habitability_model.py` - Optimizes the Gradient Boosting model for habitability indexing.
3.  **Discovery Engine**: `src/discovery/planet_discovery_engine.py` - Executes batch inference and computes the Composite Discovery Score.
4.  **Explainability Engine**: `src/ml_models/explainability_engine.py` - Calculates SHAP values to interpret model decisions globally and locally.
5.  **Insight Engine**: `src/analytics/insight_engine.py` - Generates astrophysical correlations and trend visualizations.
6.  **Summary Generation**: `src/analytics/discovery_summary_generator.py` - Produces the final executive research summary report.

## Technology Stack

*   **Logic**: Python 3.9+
*   **Database**: PostgreSQL with SQLAlchemy ORM
*   **Machine Learning**: Scikit-Learn (Gradient Boosting), NumPy, Pandas
*   **Explainability**: SHAP (Shapley Additive Explanations)
*   **Visualization**: Plotly, Matplotlib, Seaborn
*   **Frontend**: Streamlit
*   **Deployment**: Docker, Docker Compose

## Repository Structure

*   `src/data_analysis/`: Modules for data cleaning, enrichment, and quality diagnostics.
*   `src/ml_models/`: ML pipeline definitions, model artifacts, and explainability logic.
*   `src/discovery/`: Discovery ranking algorithms and batch inference engines.
*   `src/analytics/`: Scientific insight generators and executive reporting utilities.
*   `src/frontend/`: Interactive Streamlit dashboard source.
*   `src/config/`: Centralized platform configuration and environment management.
*   `src/utils/`: Standardized logging, database connectivity, and health diagnostics.
*   `analysis_outputs/`: Dynamically generated research plots and statistical reports.
*   `pipeline_logs/`: System execution logs and detailed performance reports.
*   `docs/`: Technical documentation and system architecture diagrams.

## Getting Started

### 1. Prerequisites

*   Python 3.9 or higher
*   PostgreSQL 15 or higher
*   Docker (Optional, for containerized deployment)

### 2. Configuration

Set up your environment variables by creating a `.env` file from the provided template:

```bash
cp .env.example .env
```

Ensure the following variables are correctly configured:
*   `DB_USER`: Database username
*   `DB_PASSWORD`: Database password
*   `DB_HOST`: Database host address
*   `DB_NAME`: Target database name

### 3. Execution

Initialize the full platform pipeline to rebuild all scientific artifacts:

```bash
python run_exointel_pipeline.py
```

Launch the interactive discovery dashboard for research exploration:

```bash
streamlit run src/frontend/app.py
```

## Deployment

The ExoIntel platform is fully containerized for production consistency:

```bash
docker-compose up --build
```

Access the dashboard at `http://localhost:8501`.

## Machine Learning Methodology

The ExoIntel habitability index is derived through a supervised learning process targeting planetary similarity to Earth-like conditions.
*   **Data Processing**: Multi-stage outlier filtering using Z-score (threshold=3) and physical constraints (e.g., stellar mass < 50 Sun masses).
*   **Feature Engineering**: Derivation of the Earth Similarity Score (ESS) and Stellar Habitability Factor.
*   **Model Selection**: Gradient Boosting Regressor optimized via cross-validation for predictive stability and high R² performance.
*   **Target Scaling**: All scores are normalized to a [0, 1] range for intuitive scientific interpretation.

## Explainable AI Integration

ExoIntel prioritizes scientific transparency. By utilizing SHAP (Shapley Additive Explanations), the platform identifies exactly which astrophysical parameters—such as planetary equilibrium temperature or stellar mass—positively or negatively influence the habitability predictions. This allows researchers to validate model logic against established astronomical principles.

## Scientific Insights

The platform automatically surfaces galactic-scale trends:
*   **Stellar Correlations**: Analysis of how host star temperature correlates with planetary habitability potential.
*   **Discovery Efficacy**: Statistical evaluation of which astronomical discovery methods are most successful in identifying high-priority candidates.
*   **Distribution Analysis**: Global mapping of habitability scores across the known exoplanet catalog.

## Repository Structure

*   `src/data_analysis/`: Data cleansing and feature engineering logic.
*   `src/ml_models/`: Model training pipelines and SHAP explainability engines.
*   `src/discovery/`: Candidate prioritization and ranking algorithms.
*   `src/analytics/`: Scientific insight generators and reporting utilities.
*   `src/frontend/`: Streamlit interactive dashboard source.
*   `src/config/`: Centralized environment and platform configuration.
*   `src/utils/`: Standardized logging, database, and health utilities.
*   `docs/`: System architecture and technical documentation.
*   `analysis_outputs/`: Visualizations and statistical reports.

## Installation Instructions

### 1. Prerequisites
*   Python 3.9+
*   PostgreSQL 15+
*   Docker (Optional)

### 2. Configuration
Create a `.env` file from the template:
```bash
cp .env.example .env
```
Configure `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_NAME`.

## Usage Workflow

1.  **Initialize Pipeline**: Run the orchestrator to build the research foundation.
    ```bash
    python run_exointel_pipeline.py
    ```
2.  **Explore Dashboard**: Launch the research interface.
    ```bash
    streamlit run src/frontend/app.py
    ```

## Licensing

This project is licensed under the MIT License.

---
*ExoIntel AI Exoplanet Discovery Platform - Initial Stable Release v1.0.0*
