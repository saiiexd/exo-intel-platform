# ExoIntel Project Roadmap

The ExoIntel platform is an evolving tool designed for open astronomical research. The collaborative roadmap focuses on enhancing predictive accuracy, expanding data ingestion, and providing more robust scientific tools.

## Phase 1: Data Ingestion & Enrichment (Next 6 Months)

*   [ ] **Incorporate ESA GAIA Data:** Expand the data warehouse to include astrometric and photometric parameters from the GAIA DR3 catalog, improving stellar profiling.
*   [ ] **Spectroscopic Pipeline:** Begin development of a module capable of ingesting and handling theoretical transmission spectra for atmospheric classification.
*   [ ] **Automated Literature Extraction:** Implement an NLP pipeline capable of extracting nuanced, peer-reviewed planetary constraints from ArXiv pre-prints to supplement the NASA archive.

## Phase 2: Advanced Machine Learning Models (6 - 12 Months)

*   [ ] **Deep Learning Integration:** Transition from Gradient Boosting ensembles to deep neural networks (e.g., Autoencoders for anomaly detection of unique planetary systems).
*   [ ] **Time-Series Analysis:** Incorporate light-curve data directly into the platform to allow models to learn transit variability patterns.
*   [ ] **Bayesian Inference:** Switch the Habitability Index from a frequentist probability to a full Bayesian framework, providing rigorous uncertainty quantification for every prediction.

## Phase 3: Explainable AI & Visualization (12 - 18 Months)

*   [ ] **Interactive SHAP Dashboard:** Upgrade the React frontend to feature highly interactive, 3D visualizations of SHAP local force plots for individual planets.
*   [ ] **Causal Inference:** Transition beyond feature importance (correlation) to structural causal models to understand the physical drivers of the predictions.
*   [ ] **Public API Release:** Formalize the FastAPI endpoints, document them with Swagger/Redoc, and release a public-facing API for researchers worldwide to query ExoIntel's predictions programmatically.

## How You Can Help
Review the `contribution_workflow.md` file. We are currently actively seeking help with expanding the Data Ingestion pipeline and refining our scikit-learn preprocessing architectures!
