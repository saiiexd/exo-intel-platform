# Explainable AI (XAI)

## The Role of Explainability in Scientific Modeling
The deployment of machine learning in scientific disciplines, specifically astrophysics, mandates rigorous interpretability. "Black box" predictive models generating outputs without logical traceability hold minimal utility within peer-reviewed contexts. The ExoIntel platform integrates Explainable AI (XAI) frameworks to formally expose the decision-making logic of the habitability models, transforming statistical inference into verifiable astrobiological analysis.

## Feature Importance Calculation
The platform utilizes the SHAP (SHapley Additive exPlanations) framework, grounded in cooperative game theory, to resolve interpretation. We employ the specific `TreeExplainer` algorithm optimized for the platform's standard regression models (Random Forest/Gradient Boosted networks). 

The calculation process evaluates the entire training phase to compute explicit global feature importance. This process identifies the absolute magnitude of impact of specific variables (e.g., determining that Planetary Equilibrium Temperature typically dictates 45% of model variance across the dataset).

## Interpreting Individual Predictions
In addition to global variable importance, SHAP computes precise individual feature attributions for every specific prediction. This ensures every predicted candidate planet provides a localized explanation graph detailing exactly why a specific habitability index was established.

When observing an individual prediction overview, the XAI layer demonstrates:
*   **Positive Influences:** Variables forcing the habitability prediction upward (e.g., terrestrial-range planetary radius).
*   **Negative Influences:** Variables actively decreasing the viability metric (e.g., excessively high stellar radiation).
*   **Base Value Departure:** How these variables interact to push the model from the average baseline measurement to the specific finalized prediction.

The integration of these analyses ensures researchers can debate and technically review the AI conclusions using explicit parameter attributions.
