# ExoIntel – AI Exoplanet Discovery Platform

ExoIntel is an AI-driven research platform designed for the systematic analysis of exoplanet datasets to identify candidate planets with a high probability of habitability. By integrating machine learning, astrophysical feature engineering, and explainable AI (XAI), the platform provides a rigorous framework for transforming raw astronomical data into validated research insights.

## Project Purpose

The search for habitable exoplanets is characterized by the vast scale of observational data and the subtle signatures of potential habitability. ExoIntel addresses this challenge by providing a reproducible, automated pipeline that evaluates confirmed exoplanets based on Earth-like criteria. The platform focuses on:

- **Scientific Discovery**: Identifying priority targets for further atmospheric and biosignature observation.
- **Reproducible Research**: Ensuring that discovery rankings and model predictions are backed by auditable feature engineering and explanations.
- **Explainability**: Utilizing SHAP-based analysis to understand why specific planets are ranked as habitable, bridging the gap between "black-box" ML and astrophysical theory.

## Key Capabilities

- **Automated Data Ingestion**: Seamless retrieval of confirmed exoplanet records from the NASA Exoplanet Archive API.
- **Astrophysical Feature Engineering**: Calculation of habitability indicators including Equilibrium Temperature, Stellar Flux, and ESI (Earth Similarity Index).
- **Machine Learning Habitability Predictions**: Gradient Boosting and Random Forest models trained on planetary and stellar parameters to predict habitability indices.
- **Explainable AI (XAI)**: Comprehensive SHAP analysis providing global feature importance and local planet-level explanations.
- **Discovery Ranking Engine**: A specialized module for scoring and prioritizing the most promising habitable candidates.
- **Scientific Analytics**: Generation of trend reports and astrophysical visualizations for research dissemination.
- **Experiment Tracking**: Automated logging of model performance and hyperparameter configurations across research runs.
- **Subsystem Metrics**: Real-time monitoring of pipeline health and operational efficiency.
- **Interactive Discovery Dashboard**: A production-ready Streamlit interface for exploring candidate datasets and visualizations.
- **Research API**: A RESTful service for programmatic access to discovery results and model predictions.

## System Architecture

ExoIntel is built on a modular, layered architecture designed for scalability and research integrity:

1.  **Data Layer**: PostgreSQL data warehouse for structured storage of raw NASA data, engineered features, and discovery results.
2.  **Ingestion & Processing Layer**: Python-based modules for API interaction and astrophysical feature enrichment.
3.  **Modeling Layer**: Scikit-learn pipelines for training, evaluating, and persisting habitability prediction models.
4.  **Intelligence Layer**: The Discovery Engine for ranking and the Explainability Engine (SHAP) for generating model interpretations.
5.  **Analytics Layer**: Subsystems that synthesize pipeline outputs into formal research reports and visualizations.
6.  **Presentation Layer**: Streamlit dashboard for interactive exploration and a Research API for external integration.
7.  **Orchestration Layer**: A central management script that coordinates the full discovery workflow with health checks and logging.

## Repository Structure

```text
├── src/                        # Core system modules
│   ├── analytics/              # Insight engines and report generators
│   ├── api/                    # Research API service (FastAPI)
│   ├── config/                 # System and database configuration
│   ├── data_analysis/          # Dataset enrichment and preprocessing
│   ├── data_ingestion/         # NASA API fetchers and loaders
│   ├── discovery/              # Habitability ranking and discovery logic
│   ├── frontend/               # Interactive Streamlit dashboard
│   ├── metrics/                # Platform monitoring and system health
│   ├── ml_models/              # Model training, experiments, and XAI (SHAP)
│   └── utils/                  # Shared loggers and health checks
├── docs/                       # Architecture diagrams and research material
├── experiments/                # Model evaluation and benchmarking logs
├── benchmarks/                 # Planetary scenario testing suites
├── reports/                    # Generated research papers and summaries
├── datasets/                   # Reference datasets and transformations
├── analysis_outputs/           # Visualizations (SHAP, trends, rankings)
└── run_exointel_pipeline.py    # Main pipeline orchestrator
```

## Installation and Setup

### Prerequisites
- Python 3.9+
- PostgreSQL 14+
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/saiiexd/exo-intel-platform.git
cd exo-intel-platform
```

### 2. Environment Configuration
Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Database Setup
Ensure PostgreSQL is running and create the database specified in your environment settings. Initialize the environment variables:
```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

## Running the Platform

### Autonomous Discovery Pipeline
The orchestrator manages the full research workflow. Run the following command to execute the production pipeline:
```bash
python run_exointel_pipeline.py
```
To run the full suite including data refresh and research experiments:
```bash
python run_exointel_pipeline.py --run-all
```

### Interactive Discovery Dashboard
Launch the visualization frontend to browse candidate planets:
```bash
streamlit run src/frontend/app.py
```

### Research API Service
Start the API to access discovery insights programmatically:
```bash
python -m src.api.main
```

## Using the Platform

- **Candidate Exploration**: Use the Streamlit dashboard to filter planets by habitability score, stellar type, or distance. View individual planet "Report Cards" with SHAP explanations.
- **Analysis Outputs**: Review the `analysis_outputs/` directory for high-resolution plots of feature importance and planetary distributions.
- **Reporting**: Automated summaries and research snapshots are exported to the `reports/` folder after each pipeline execution.

## Research Workflow

ExoIntel implements a "Scientific-as-Code" workflow:
1.  **Ingestion**: Fetch latest confirmed exoplanets from NASA.
2.  **Enrichment**: Apply astrophysical formulas for habitability indicators.
3.  **Inference**: Run trained Gradient Boosting models to predict scores.
4.  **Explain**: Generate SHAP values for every inference to ensure theoretical alignment.
5.  **Rank**: Sort candidates and generate the discovery short-list.
6.  **Disseminate**: Produce visual and textual research reports.

## Interactive Web Interface

The ExoIntel platform includes a dedicated interactive web interface built with React and TypeScript. This interface provides a robust, component-driven frontend application that enables researchers and users to explore discovery datasets and interact directly with the predictive models.

The frontend integrates seamlessly with the ExoIntel platform by communicating with the backend FastAPI service via RESTful endpoints. This architecture decouples the presentation layer from the data warehouse and machine learning pipelines, ensuring a scalable and maintainable system. All data fetching operations handle loading states and include safe fallbacks in case the backend API is temporarily unavailable.

### Running the Frontend Locally

To launch the interactive web interface on your local machine, follow these steps:

1. Clone the repository
2. Navigate to the frontend directory: `cd frontend`
3. Install dependencies: `npm install`
4. Run the development server: `npm run dev`

### Interface Features

The application provides the following core pages:

* **Home**: Displays high-level platform statistics, navigational elements, and an overview of the scientific methodology powering the autonomous discovery engine.
* **Discovery Explorer**: A comprehensive data table for browsing candidate planets, featuring search capabilities, filtering mechanisms, and detailed habitability scores derived from the backend models.
* **Habitability Simulator**: An interactive environment where users can manipulate planetary parameters (such as radius, mass, and equilibrium temperature) and invoke the prediction service to receive a habitability consensus score.
* **AI Insights**: Presents scientific visualizations and global feature importance metrics extracted from the explainable AI (SHAP) layer, illustrating model behavior and correlation patterns.
* **Research**: Contains formal documentation regarding system architecture, autonomous pipeline workflows, and links to the project's technical documentation.

This frontend application complements the existing Streamlit research dashboard. While the Streamlit dashboard serves as an internal tool optimized for rapid data visualization and direct Python integration during model development, the React frontend delivers a highly responsive, scalable, and user-friendly experience intended for broader external engagement and presentation of final discovery results.

## Contributing

We welcome contributions from the astrophysics and machine learning communities.
1.  **Fork** the repository.
2.  Create a **Feature Branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your changes (`git commit -m 'Add some AmazingFeature'`).
4.  **Push** to the branch (`git push origin feature/AmazingFeature`).
5.  Open a **Pull Request**.

Ensure that new features include appropriate tests and documentation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
