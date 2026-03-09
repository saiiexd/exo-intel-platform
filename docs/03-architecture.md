# Architecture

## Technical Architecture Description
The ExoIntel platform employs a modular, microservices-oriented architecture designed to scale robustly while maintaining strict separation of concerns. This design facilitates independent development, testing, and deployment of each distinct subsystem.

## Component Responsibilities and Interactions

### Data Ingestion Modules
The ingestion layer consists of specialized Python scripts responsible for querying the NASA Exoplanet Archive via robust REST implementations. This component manages API rate limiting, handles pagination, and performs preliminary validation of the JSON payload before passing the raw data downstream.

### PostgreSQL Warehouse
The central data repository is a PostgreSQL relational database. It is engineered with strict schema validation to enforce data integrity. The database acts as the single source of truth connecting the ingestion pipelines, the machine learning models, and the frontend interfaces, isolating data storage from application logic.

### Feature Engineering Pipeline
This module serves as the critical transformation layer. Implemented in Python using the Pandas framework, it normalizes numerical variables, imputes missing data points, and derives advanced astrobiological features from primitive metrics. It processes data directly extracted from the warehouse and returns cleanly formatted datasets ready for inference.

### Machine Learning Models
The predictive core is built upon scikit-learn tree-based ensemble methods, specifically Gradient Boosting and Random Forest architectures. The models are serialized and version-controlled. They interface strictly with the feature-engineered dataset to output the computed habitability metric.

### Discovery Engine
Operating as a specialized execution layer subsequent to the machine learning inference, the discovery engine applies heuristic adjustments. It merges the habitability predictions with Earth Similarity Index (ESI) approximations and structural parameters to rank the planetary dataset rigorously.

### Explainability Modules
The explainability layer utilizes the SHAP (SHapley Additive exPlanations) library. It independently evaluates the trained machine learning model and the engineered features to produce local interpretations for individual predictions, generating the graphical artifacts required to establish scientific transparency.

### Insight Generation Layer
This analytical component parses aggregate results from the discovery engine. It specializes in broad statistical visualization, creating histograms, correlation matrices, and distribution metrics. It acts as an intermediary layer supplying pre-computed insights to the presentation layers.

### Automated Pipeline Orchestrator
The `run_exointel_pipeline.py` script serves as the primary system orchestrator. It manages the execution sequence, logging, error handling, and dependency resolution between all sequential modules (ingestion, processing, inference, and visualization output initialization).

### Streamlit Dashboard
The Streamlit interface functions as an immediate, analytical frontend. It directly queries the PostgreSQL backend and local graphical assets to render interactive charts designed for researchers needing rapid data exploration and statistical review.

### React Frontend
The React application constitutes the external-facing user interface. Served by a distinct development server, it consumes backend APIs to present a polished, highly interactive exploratory experience geared towards presenting the final discovery rankings and clear SHAP explanations.
