# ExoIntel Scientific Methodology Report

## 1. Introduction: Exoplanet Habitability Prediction
The discovery of habitable exoplanets is a primary objective of modern astrophysics. ExoIntel leverages machine learning to prioritize targets within the growing catalog of verified exoplanets by estimating their similarity to terrestrial life-hosting conditions.

## 2. Dataset Description & Preprocessing
Data is sourced from the NASA Exoplanet Archive (TAP sync).
- **Outlier Filtering**: Statistical removal of observations with Z-scores > 3 in key physical parameters (radius, mass, temperature).
- **Physical Constraints**: Exclusion of physically improbable host-star configurations (e.g., mass > 50 $M_\odot$).
- **Balancing**: Oversampling of rare candidate types to prevent model bias toward ubiquitous but non-habitable gas giants.

## 3. Feature Engineering Methodology
ExoIntel derives advanced astrophysical metrics to enhance model sensitivity:
- **Earth Similarity Score (ESS)**: A composite physical index based on geocentric similarity.
- **Stellar Habitability Factor (SHF)**: Evaluates the parent star's suitability based on Spectral Class and Luminosity.
- **Density Normalization**: Corrects for composition variance relative to Earth's silicate-iron bulk.

## 4. Machine Learning Model Architecture
- **Algorithm**: Gradient Boosting Regressor (GBM).
- **Optimization**: Hyperparameter tuning via 5-fold cross-validation.
- **Evaluation**: Benchmarked against RandomForest and Linear baselines using R² and RMSE.

## 5. Explainable AI Integration (SHAP)
Utilizes Shapley Additive Explanations to decompose the "black box" of the GBM model.
- **Global Importance**: Surfaces the primary physical drivers of predicted habitability across the catalog.
- **Local Explanations**: Provides feature-level waterfalls for individual priority candidates (e.g., Proxima Cen b).

## 6. Scientific Insights & Findings
The analytics engine identifies high-level trends:
- **M-Dwarf Efficacy**: Evaluation of the "M-Dwarf Opportunity" within current discovery methods.
- **Candidate Clustering**: Regional mapping of habitable zones within the Solar Neighborhood.

## 7. Limitations & Future Directions
- **Biosignature Data**: Current models lack spectroscopic atmospheric data.
- **Future Integration**: Planned integration of JWST atmospheric composition metrics for high-ESS candidates.
