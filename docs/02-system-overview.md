# System Overview

## High-Level Lifecycle
The ExoIntel platform operates as an end-to-end data processing and analysis pipeline. The system lifecycle is structured sequentially to ensure data integrity, consistent model training, and accurate discovery ranking.

The complete workflow comprises the following phases:
1. **Data Ingestion**
2. **Data Engineering and Storage**
3. **Machine Learning Training and Inference**
4. **Discovery Ranking**
5. **Visualization and Interactivity**

## Narrative of Data Flow
Data flows through the system beginning as disparate records and concluding as ranked, highly interpretable scientific candidates.

### 1. External Acquisition
The platform interface invokes an automated extraction routine that queries the NASA Exoplanet Archive API. Raw datasets containing physical planetary parameters, stellar attributes, and discovery metrics are retrieved via secure HTTP connections and initially serialized into localized storage to ensure uninterrupted subsequent processing.

### 2. Processing and Warehouse Loading
The data engineering module parses the raw dataset, handling null values and aligning unit measurements. Complex feature engineering is applied to calculate composite metrics, such as equilibrium temperatures and orbital eccentricities, necessary for predicting planetary conditions. The enriched dataset is subsequently committed to a relational PostgreSQL warehouse, ensuring a structured schema optimized for querying by analytics engines.

### 3. Model Application
The machine learning subsystem retrieves the structured records from PostgreSQL. Following categorical encoding and scaling, the data is passed into the trained prediction model. The model calculates a probabilistic habitability index for each planetary record. Simultaneously, the explainability module calculates feature contributions for every prediction, mapping the mathematical reasoning alongside the final score.

### 4. Ranking and Insights
The generated predictions are submitted to the discovery engine. The engine computes a composite ranking score balancing the raw habitability index with astrophysical similarity metrics relative to Earth. The final results isolate the most promising candidate planets. The insight generation layer then processes this refined dataset to compute aggregate statistics, identifying global correlations and distribution trends.

### 5. Final Presentation
The completed datasets, rankings, and analytical outputs are exposed to dual interfaces. The Streamlit research dashboard provides a static, exploratory view for deep-dive analysis of global trends, while the React interactive frontend provides a dynamic user interface for querying specific planets and reviewing complex SHAP interpretations.
