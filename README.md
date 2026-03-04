# ExoIntel Data Platform

AI‑powered exoplanet analytics backend and data pipeline.

## Structure

```
exo-intel-platform/
├── data/
│   ├── raw/
│   └── processed/
├── migrations/
├── src/
│   ├── ingestion/            # data ingestion scripts
│   ├── ml_models/            # model training & prediction
│   ├── ai_assistant/         # LLM based SQL assistants
│   └── utils/                # shared utilities (DB connections, etc.)
├── notebooks/                # exploratory notebooks
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

1. Create a Python environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. Ensure a PostgreSQL database named `exo_intel_db` is available and the
   connection string in `src/utils/db.py` is configured appropriately.

3. Run ingestion script to populate the warehouse:
   ```bash
   python -m src.ingestion.ingest_exoplanet_data
   ```

4. Train or load the habitability model:
   ```bash
   python -m src.ml_models.habitability_model_v1
   ```

5. Start API servers:
   ```bash
   uvicorn src.api.habitability_api:app --reload
   uvicorn src.api.ai_query_api:app --reload
   ```

6. Use the assistant CLI tools under `src/ai_assistant` for interactive queries.
