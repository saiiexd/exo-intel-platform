# Running the Platform

## Execution Protocols
This document establishes the formal commands required to execute the ExoIntel architecture, triggering the data ingestion pipeline, model inference, and local interface hosting.

## Executing the Automated Pipeline
The core processing logic is fully encapsulated within a single orchestration script. Executing this file performs data retrieval from the NASA API, engineers all necessary features, trains and invokes the predictive model, updates the PostgreSQL database, and generates required Explainable AI visualizations.

Ensure the Python virtual environment is active and the PostgreSQL instance is functional, then execute:

```bash
python run_exointel_pipeline.py
```
*Note: This process is computationally extensive and may require several minutes depending on the target system hardware and the current volume of the exoplanet archive dataset.*

## Launching the Streamlit Research Dashboard
To initialize the scientific analysis frontend for immediate statistical review, invoke the Streamlit server from the root repository:

```bash
streamlit run src/frontend/app.py
```
This commands instantiates a local server, automatically opening the interactive dashboard inside the default web browser (typically on port 8501).

## Launching the React Development Server
The primary interactive exploration interface requires the Node.js development server to compile and host the React application. Address this microservice independently by navigating to the frontend directory:

```bash
cd frontend
npm run dev
```
This initiates a hot-reloading web node (typically hosted on port 3000 or 5173), providing the fully stylized user experience to query the backend database and review candidate planet profiles.
