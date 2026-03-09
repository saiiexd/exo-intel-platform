# Data Pipeline

## Data Ingestion and Engineering Process
The data pipeline represents the foundational component of the ExoIntel architecture. It guarantees the reliable extraction of planetary data, rigorously enforces quality standards, and facilitates the mathematical transformations required to feed complex machine learning operations.

## Connection to the NASA Exoplanet Archive
The pipeline initializes by establishing an automated HTTP connection to the NASA Exoplanet Archive's Table Access Protocol (TAP) service. The system issues specific ADQL (Astronomical Data Query Language) commands to retrieve confirmed planetary records. The query limits the returned columns to essential astrometric, photometric, and physical properties required for habitability assessment.

## Retrieving and Processing Raw Datasets
Once the API responds, the raw payload (typically received in JSON or CSV format) undergoes parsing. The initial script cleans formatting errors, standardizes naming conventions across varying discovery facilities, and discards partial records missing critical identification markers.

## Feature Engineering Methods
The raw parameters are subjected to an extensive feature engineering process, crucial for modeling planetary habitability:
*   **Imputation Techniques:** Missing values in key physical descriptors (such as planetary mass or stellar radius) are conditionally imputed based on correlation models derived from similar planetary classes.
*   **Derived Metrics:** The pipeline calculates composite values. Crucially, estimated equilibrium temperature (Teq) is consistently calculated based on stellar luminosity and semi-major orbital axis when absent from the archive dataset.
*   **Normalization:** Logarithmic scaling and min-max normalization are applied to features featuring high variance (e.g., planetary mass and orbital periods) to ensure stable model convergence during the machine learning phase.

## PostgreSQL Database Storage
Post-processing, the enriched dataset is committed to the PostgreSQL warehouse. The database utilizes a well-defined schema (`exoplanet_data` tables). Storing the processed dataset in a relational format ensures that both the inference engines and frontend visualization tools can query massive data subsets highly efficiently using standard SQL interfaces.
