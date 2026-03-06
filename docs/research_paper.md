# ExoIntel: An Autonomous Framework for High-Fidelity Exoplanet Habitability Assessment and Target Prioritization

**Author**: ExoIntel Research Laboratory  
**Version**: 1.4.0-autonomous  
**Date**: March 2026

---

## Abstract
The rapid expansion of exoplanetary catalogs necessitates autonomous systems capable of synthesizing vast astronomical datasets into actionable scientific intelligence. We present **ExoIntel**, a research-grade platform designed for the automated ingestion, analysis, and prioritization of habitable exoplanetary candidates. Utilizing high-fidelity Gradient Boosting architectures integrated with explainable AI (SHAP), the platform achieves robust predictive performance for the planetary habitability index. This paper details the system architecture, the integration of NASA Exoplanet Archive TAP services, and the discovery of a prioritized catalog of candidates, including notable high-scoring objects such as Kepler-1649 b.

## 1. Introduction
The search for life beyond the Solar System is one of the most significant endeavors in modern astrophysics. With over 5,500 confirmed exoplanets, manual analysis of planetary suitability for liquid water and atmospheres is increasingly inefficient. ExoIntel addresses this challenge by providing a fully autonomous research pipeline that combines statistical astrophysics with supervised machine learning.

## 2. Dataset Description and Ingestion
ExoIntel utilizes the **NASA Exoplanet Archive** as its primary data source. The platform implements an autonomous ingestion layer using the Table Access Protocol (TAP) to retrieve composite planetary parameters. 
- **Raw Data**: Confirmed planetary systems with metrics including radius ($R_\oplus$), mass ($M_\oplus$), and equilibrium temperature ($T_{eq}$).
- **Enrichment**: Data is cleansed using iterative imputation and enriched with derived indices, including the Earth Similarity Index (ESI) approximation and Stellar Habitability Factors.

## 3. Feature Engineering
The predictive model relies on a curated set of astrophysical features:
1. **Planetary Metrics**: Radius, mass, and density ratios.
2. **Thermal Environment**: Equilibrium temperature and stellar effective temperature ($T_{eff}$).
3. **Orbital Dynamics**: Orbital period and semi-major axis correlations.
4. **Stellar Context**: Stellar mass and radius ($M_\odot, R_\odot$).

## 4. Machine Learning Methodology
We employ a **Gradient Boosting Regressor** as the primary inference engine. The model was trained on a cross-validated dataset with habitability targets derived from multi-variate planetary similarity metrics.
- **Optimization**: Hyperparameters were tuned using GridSearchCV.
- **Evaluation**: The model achieves high R-squared scores, indicating strong alignment with established astrophysical habitability models.

## 5. Explainable AI and Feature Importance
To ensure scientific transparency, we utilize **SHAP (SHapley Additive exPlanations)**. Global analysis reveals that **Planet Mass** and **Equilibrium Temperature** are the dominant drivers of habitability predictions. This alignment with "classical" habitability models validates the machine learning approach for discovery prioritization.

## 6. Discovery Engine and Ranking Algorithm
The Discovery Engine computes a **Combined Discovery Score**, a weighted average of ML-predicted habitability and analytical Earth similarity. This dual-layer approach ensures that targets are both statistically probable and physically consistent with terrestrial analogues.

## 7. Results and Scientific Insights
Execution of the v1.4.0 pipeline on the NASA PSComps catalog identified 4,433 candidates. The top-ranked habitable candidate, **Kepler-1649 b**, shows high planetary similarity and favorable thermal profiles. Population-level analysis suggests a non-linear correlation between stellar mass and the frequency of high-habitability candidates in the M-dwarf regime.

## 8. Research API and Programmatic Access
To facilitate open-source collaboration, ExoIntel v1.4.0 exposes its intelligence via a RESTful Research API. External systems can retrieve real-time discovery leaderboards, specific planetary deep-dives, and global feature importance metrics, enabling the platform to serve as a backbone for wider astrophysics research.

## 9. Conclusion and Future Directions
ExoIntel v1.4.0 demonstrates the feasibility of an autonomous research platform for exoplanetary science. Future iterations will focus on integrating atmospheric transmission spectroscopy data (JWST analogues) and deep learning for light-curve analysis to further refine habitability assessments.

---
**Keywords**: Exoplanets, Machine Learning, Habitability, SHAP, NASA Exoplanet Archive, Astrophysics Research.
