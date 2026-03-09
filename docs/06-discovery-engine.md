# Discovery Engine

## Discovery Ranking System
The discovery engine acts as the capstone evaluation layer within the computational pipeline. While the machine learning model executes raw predictions regarding habitability probability, the discovery engine contextualizes these predictions, sorting the planetary database into a structured ranking format optimized for detailed research targeting.

## Combining Predictions with Astrophysical Similarity
Habitability relies on a complex interplay of variables. Consequently, relying exclusively on an isolated machine learning prediction limits perspective. The discovery engine resolves this by integrating the output habitability index with an independent Earth Similarity Index (ESI) approximation metric. This composite approach ensures that highly ranked candidates not only exhibit theoretical habitability bounds based on the model training but structurally and dimensionally mirror proven conditions.

## The Discovery Scoring Mechanism
The final rank score is calculated via an integrated weighting equation. The standard mechanism operates under the following conditions:
*   **Base Weighting:** The machine learning prediction forms the primary basis of the score.
*   **Similarity Modifiers:** Variances in radius, mass, and equilibrium temperature relative to Earth normals dynamically adjust the baseline score.
*   **Penalization Execution:** Planets existing precisely on the boundaries of the classical habitable zone with high orbital eccentricity encounter mild score penalization to account for periodic extreme temperatures.

## Identifying Candidates
Following the execution of the score mechanism, the planetary repository is sorted iteratively. The engine isolates subsets categorized into primary tiers (e.g., highly probable candidates, borderline candidates, low viability planets). The leading candidate list is automatically designated, recorded in the database, and serialized for immediate ingestion by both the analytical dashboards and interactive interfaces.
