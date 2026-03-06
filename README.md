# ExoIntel: A Reproducible AI-Driven Astrophysics Research Platform

ExoIntel is an advanced, production-grade research platform designed for the automated discovery, scientific characterization, and habitability assessment of exoplanets. Developed to meet high standards of scientific reproducibility, the platform integrates astrophysical feature engineering, multi-algorithm machine learning benchmarks, and SHAP-based explainable AI (XAI).

## Scientific Motivation

The identification of habitable environments beyond our solar system is a critical challenge in modern astrophysics. ExoIntel addresses this by providing a unified, extensible framework for:
*   **Predictive Taxonomy**: Identifying high-priority candidates using advanced Gradient Boosting architectures.
*   **Physical Similarity Assessment**: Quantifying Earth-similarity through derived indices (ESS, SHF).
*   **Model Transparency**: Decomposing machine learning "black box" decisions into interpretable physical contributions via SHAP value analysis.
*   **Reproducible Experimentation**: Maintaining a versioned record of data transformations and model benchmarks.

## Platform Architecture & Research Workflow

ExoIntel is structured to mirror the scientific method, from raw observation to formal peer-ready reporting.

### 1. Research-Grade Directory Structure
*   `datasets/`: Versioned snapshots of raw, cleaned, and enriched planetary catalogs.
*   `experiments/`: Performance logs and multi-algorithm benchmark comparisons.
*   `benchmarks/`: Evaluation of model consistency against standardized planetary profiles.
*   `reports/`: Formal scientific methodology and research findings.
*   `results/`: Aggregated discovery leaderboards and population statistics.
*   `src/`: Core implementation packages for the pipeline and dashboard.

### 2. The Discovery Pipeline
The system orchestrates data flow through five critical stages:
1.  **Ingestion & Diagnostics**: Retrieval from NASA Exoplanet Archive with statistical outlier detection.
2.  **Astro-Feature Engineering**: Derivation of Earth Similarity Scores and Stellar Habitability Factors.
3.  **Model Benchmarking**: Comparison of Random Forest, Gradient Boosting, and Linear architectures.
4.  **Explainability Analysis**: Generation of SHAP global impact and candidate-level waterfall plots.
5.  **Scientific Insights**: Synthesis of astrophysical trends and discovery method efficacy.

## Reproducing the Research Workflow

### Prerequisites
*   Python 3.9+ | PostgreSQL 15+ | Docker (Optional)

### Installation & Execution
```bash
# 1. Clone & Configure
git clone https://github.com/saiiexd/exo-intel-platform.git
cp .env.example .env # Configure database credentials

# 2. Execute Full Research Pipeline
# Rebuilds datasets, runs experiments, benchmarks, and generates reports
python run_exointel_pipeline.py --run-all

# 3. Explore Insights
streamlit run src/frontend/app.py
```

## Machine Learning Methodology

ExoIntel employs a supervised learning strategy optimized for predictive stability:
*   **Pre-processing**: Min-Max scaling of target variables and Z-score outlier removal (N=3).
*   **Optimization**: 5-fold cross-validation with grid-search hyperparameter tuning.
*   **Validation**: Benchmarked against 'Earth Baseline' and 'Hot Jupiter' scenarios to ensure physical consistency.

## Scientific Reporting & Results

*   **Methodology Report**: Detailed overview of feature derivation and model selection logic in `reports/scientific_methodology.md`.
*   **Discovery Leaderboard**: Ranked prioritize of promising candidates updated during each pipeline execution.

---
*ExoIntel AI Exoplanet Discovery Platform - v1.3.0 Research Grade*
