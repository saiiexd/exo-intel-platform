# Machine Learning Methodology

This document details the Machine Learning (ML) architecture powering the ExoIntel platform, from data ingestion through continuous evaluation.

## 1. Workflow Architecture

The ExoIntel ML pipeline is designed for robustness, automated execution, and scientific reproducibility. The core workflow follows a standard end-to-end architecture:

1.  **Data Ingestion & Validaton:** Fetch raw astronomical data.
2.  **Preprocessing Pipeline:** Handle nulls, impute missing values, and normalize features using `MinMaxScaler` bound between [0, 1].
3.  **Feature Engineering:** Generate composite metrics (ESS, Density Ratios, Spectral flags).
4.  **Model Training & Tuning:** Multi-algorithm evaluation utilizing GridSearchCV.
5.  **Evaluation & Serialization:** Metric calculation and caching of the best performer as a `pipeline.pkl` artifact.
6.  **Explainability Analysis:** Post-hoc SHAP value generation for interpretability.

## 2. Preprocessing and Feature Engineering

The `scikit-learn` Pipeline architecture is utilized to ensure that no data leakage occurs between the training and testing sets. 
- **Numerical Pipelines:** Utilize `SimpleImputer(strategy='median')` followed by `MinMaxScaler`.
- **Categorical Pipelines:** (e.g., Stellar Spectral Types) utilize `OneHotEncoder(handle_unknown='ignore')`.

Target variables (like the normalized pseudo-habitability index used for regression training) are strictly isolated during the transformation phase to prevent target leakage.

## 3. Model Training Strategy

ExoIntel evaluates multiple algorithmic architectures to select the optimal model for habitability ranking. Primarily, the system focuses on tree-based ensembles due to their robustness against unscaled variance and non-linear astrophysical relationships.

### Primary Algorithms
*   **Random Forest Regressors:** Provide excellent baseline performance and natural feature importance extraction through variance reduction calculations.
*   **Gradient Boosting (XGBoost/LightGBM):** Frequently selected as the optimal model by the orchestration engine due to their ability to sequentially minimize pseudo-residuals on complex, interconnected planetary features.

### Hyperparameter Tuning
We employ `GridSearchCV` with robust 5-fold cross-validation. Typical hyperparameter search spaces include:
*   `n_estimators`: [100, 200, 300]
*   `max_depth`: [5, 10, None]
*   `min_samples_split`: [2, 5, 10]
*   `learning_rate` (for boosting): [0.01, 0.1, 0.2]

## 4. Evaluation Metrics

Because habitability modeling in this context acts primarily as a regression and ranking task, the models are evaluated using standard regression diagnostics:

-   **R² (Coefficient of Determination):** Measures the proportion of variance in the habitability index predictable from the features.
-   **RMSE (Root Mean Squared Error):** Provides a direct measurement of prediction error magnitude in the same units as the target variable.
-   **MAE (Mean Absolute Error):** Offers a robust metric less sensitive to severe outliers (which are common in deep-space astronomical datasets).

## 5. Explainable AI Techniques

Scientific models mandate transparency. We utilize the **SHAP (SHapley Additive exPlanations)** library, specifically the `TreeExplainer`, which is highly optimized for ensemble methods.

SHAP calculates the exact marginal contribution of every feature to a specific prediction. This allows ExoIntel to generate:
*   **Global Summary Plots:** Showing which features (e.g., Equilibrium Temp or Radius) drive the model's overall logic.
*   **Local Force Plots:** Explaining exactly *why* a specific planet (e.g., Proxima Centauri b) received its specific habitability score, increasing trust and guiding future astrobiological hypotheses.
