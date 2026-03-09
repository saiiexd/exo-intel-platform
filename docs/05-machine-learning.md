# Machine Learning Workflow

## Habitability Prediction Overview
The core predictive capability of the ExoIntel platform relies on a sophisticated machine learning workflow designed to estimate planetary habitability. The objective is to assign a probabilistic index (ranging entirely from 0.0 to 1.0) defining the likelihood of a candidate planet maintaining life-supporting conditions.

## Model Features
The predictive model relies on an assortment of specific, scientifically verified features engineered directly from the data pipeline. Critical features include:
*   **Planetary Radius and Mass:** Determine whether a planet is terrestrial or gaseous.
*   **Equilibrium Temperature:** Evaluates if surface temperatures allow for the existence of liquid water.
*   **Orbital Eccentricity:** Tracks temperature variance throughout the planetary orbit.
*   **Stellar Variables:** Encompasses stellar mass, effective temperature, and metallicity to gauge the stability and output of the host star.

## Preprocessing Steps
Consistent with formal data science methodologies, the data undergoes specific final transformations prior to training initialization. Independent variables are standardized using robust scaling methodologies to mitigate the impact of astrophysical outliers. Categorical variables, such as specific stellar spectral types, are handled via one-hot encoding frameworks.

## Model Training Pipeline
The platform leverages a tree-based ensemble methodology. Primarily utilizing scikit-learn's `RandomForestRegressor` and potentially `GradientBoostingRegressor`, the models traverse the engineered dataset. Hyperparameter tuning is executed via formal Grid Search methodologies with cross-validation protocols to restrict model variance and overfitting. An integrated pipeline object encapsulates the scaling rules alongside the finalized model infrastructure to ensure inference consistency.

## Evaluation Methodology
The trained pipeline undergoes rigorous evaluation using independent testing sets isolated during the preprocessing phase. The performance metrics prioritized by the system include:
*   **R² Score (Coefficient of Determination):** To assess the proportion of variance handled by the model.
*   **Root Mean Squared Error (RMSE):** To quantify standard prediction deviance.
*   **Mean Absolute Error (MAE):** To track pure prediction error magnitude without penalizing outliers excessively.

## Algorithm Selection Rationale
Ensemble decision tree models demonstrate significant advantages over neural architectures for this specific domain. Primarily, they manage the non-linear astrophysics dependencies effectively while mitigating the impact of missing or heavily imputed astronomical data. Furthermore, tree-based models integrate seamlessly with established Explainable AI (XAI) frameworks like SHAP, which is mandatory for ensuring full methodological transparency.
