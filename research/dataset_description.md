# Dataset Description and Feature Engineering

This document outlines the structure, origin, and transformation of the datasets utilized by the ExoIntel platform.

## Raw Data Ingestion

The foundational dataset is sourced directly from the **NASA Exoplanet Archive** via its active TAP (Table Access Protocol) service. This API provides the most updated, peer-reviewed parameters for all confirmed exoplanets and strong candidates.

### Key Raw Features
The raw ingestion process extracts several critical physical and orbital parameters:
*   `pl_name`: Planet Name
*   `discoverymethod`: Method of discovery (e.g., Transit, Radial Velocity)
*   `disc_year`: Discovery Year
*   `sy_dist`: Distance from Earth (parsecs)
*   `pl_rade`: Planetary Radius (in Earth radii)
*   `pl_masse`: Planetary Mass (in Earth masses)
*   `pl_orbper`: Orbital Period (days)
*   `pl_orbsmax`: Orbital Semimajor Axis (AU)
*   `pl_eqt`: Planetary Equilibrium Temperature (K)
*   `st_teff`: Stellar Effective Temperature (K)
*   `st_rad`: Stellar Radius (Solar radii)
*   `st_mass`: Stellar Mass (Solar masses)
*   `st_lum`: Stellar Luminosity (log(Solar))

## Data Cleaning and Imputation

Astronomical datasets are notoriously sparse. To prepare the data for machine learning, ExoIntel applies a rigorous cleaning protocol:
1.  **Threshold Filtering:** Removal of entries missing critical target variables (e.g., both radius and mass missing).
2.  **Outlier Rejection:** Application of Z-score and Interquartile Range (IQR) methods to remove physically impossible sensor anomalies.
3.  **Intelligent Imputation:** Utilizing correlation matrices (e.g., Mass-Radius relationships) to impute missing values where scientifically justifiable.

## Feature Engineering Process

Raw data, while valuable, often fails to capture the complex interdependencies required to predict habitability. ExoIntel executes a feature engineering pipeline to create synthetic, higher-order variables that models can leverage more effectively.

### Engineered Features

| Engineered Feature | Derivation / Formula | Scientific Motivation |
| :--- | :--- | :--- |
| **Earth Similarity Score (ESS)** | $1 - \sqrt{\frac{(1-R/R_E)^2 + (1-M/M_E)^2}{2}}$ | Provides a baseline metric defining how "Earth-like" a planet is in bulk physical dimensions. |
| **Stellar Habitability Factor** | $L_{star} / (d^2)$ (Insolation approximation) | Estimates the relative radiation environment compared to the Solar System. |
| **Zone Flag** | Boolean derived from `pl_eqt` (e.g., $200K < T_{eq} < 320K$) | A rough, traditional "Goldilocks" cutoff used as a baseline feature for tree models to branch upon. |
| **Density Ratio** | $M_{planet} / (R_{planet})^3$ normalized to Earth | Helps the model distinguish between dense, rocky terrestrial planets and low-density gas dwarfs/giants. |

These enriched features form the final dataset (`planets_enriched.csv`) used to train the gradient boosting ensembles and generate the final candidate rankings.
