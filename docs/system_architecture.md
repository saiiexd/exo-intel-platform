# ExoIntel System Architecture

This document describes the high-level architecture and data flow of the ExoIntel AI Exoplanet Discovery Platform.

## Architecture Diagram

The following Mermaid diagram illustrates the platform's modular structure and the automated pipeline flow.

```mermaid
graph TD
    %% Orchestrator Layer
    subgraph Orchestrator_Layer ["Pipeline Control"]
        Orchestrator["Automated Pipeline Orchestrator (run_exointel_pipeline.py)"]
    end

    %% Data Layer
    subgraph Data_Layer ["Data Management"]
        DB[("PostgreSQL Data Warehouse")]
        RawData["Raw Exoplanet Data"]
    end

    %% Processing Layer
    subgraph Processing_Layer ["Processing & ML"]
        Analysis["Dataset Analysis & Feature Engineering (dataset_analysis.py)"]
        Training["ML Model Training (train_habitability_model.py)"]
        Discovery["Planet Discovery Engine (planet_discovery_engine.py)"]
    end

    %% Analysis Layer
    subgraph Analysis_Layer ["Explainability & Insights"]
        SHAP["Explainable AI (SHAP) (explainability_engine.py)"]
        Insights["Scientific Insight Engine (insight_engine.py)"]
        Summary["Discovery Summary Generator (discovery_summary_generator.py)"]
        Reports["analysis_outputs (Plots & Analytics)"]
    end

    %% Frontend Layer
    subgraph Frontend_Layer ["User Interface"]
        Streamlit["Streamlit Exploration Interface (app.py)"]
    end

    %% Data Flows
    Orchestrator -- "1. Triggers clean/enrich" --> Analysis
    Orchestrator -- "2. Triggers training" --> Training
    Orchestrator -- "3. Triggers ranking" --> Discovery
    Orchestrator -- "4. Triggers SHAP" --> SHAP
    Orchestrator -- "5. Triggers charts" --> Insights
    Orchestrator -- "6. Triggers summary" --> Summary

    RawData --> Analysis
    Analysis --> DB
    DB -- "Enriched Data" --> Training
    Training -- "habitability_model.pkl" --> Discovery
    DB -- "Planetary Metrics" --> Discovery
    Discovery --> DB
    
    Discovery -- "Predictions" --> SHAP
    Training -- "Model" --> SHAP
    SHAP -- "Feature Importance" --> DB
    SHAP --> Reports
    
    DB -- "Analytics" --> Insights
    Insights --> Reports
    Insights -- "Aggregates" --> DB

    DB -- "Final Statistics" --> Summary
    Summary --> Reports

    DB --> Streamlit
    Reports --> Streamlit
    Orchestrator -- "Execution Reports" --> Logs["pipeline_logs/"]
```

## Component Descriptions

| Component | Responsibility |
| :--- | :--- |
| **Automated Orchestrator** | Coordinates the sequential execution of the entire pipeline, ensuring data consistency and measuring performance. |
| **PostgreSQL DB** | Central source of truth for raw datasets, feature-engineered tables, discovery rankings, and analytics metrics. |
| **Dataset Analysis** | Cleans raw astronomical data, handles missing values, and computes physics-based metrics like Earth Similarity. |
| **ML Training** | Trains a Gradient Boosting Regressor (or Random Forest) to predict habitability scores based on planetary signatures. |
| **Discovery Engine** | Performs batch inference on the entire catalog to rank and prioritize the most promising exoplanet candidates. |
| **Explainable AI (SHAP)** | Breaks down model "black box" decisions into interpretable feature contributions using SHAP values. |
| **Scientific Insight Engine** | Generates high-level astrophysical visualizations and correlation heatmaps for research analysis. |
| **Summary Generator** | Produces the final executive research summary report based on all pipeline findings. |
| **Streamlit Interface** | Provides an interactive, visual gateway for researchers to explore candidates and simulate habitability. |
