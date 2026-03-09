# Demo Guide

## Executing the Demonstration Environment
For presentation, rapid testing, or system validation purposes without enduring the complete multi-hour data ingest and training pipeline, the ExoIntel platform includes a specialized demonstration mode.

## Generating the Demo Dataset
The demo architecture relies on a highly truncated, statically compiled subset of the exoplanet archive containing previously verified habitability candidates alongside representative negative classifications. This circumvents API rate limits and computationally heavy feature engineering processes. The generation of this dataset is either included within the repository or managed via a designated demo initialization script.

## Executing the Demo Runner Script
To run the platform securely against the demo dataset, utilize the designated demo execution command. This bypasses the live ingestion modules, directly loading the static sample into a temporary database schema or mock ORM, executing an ultra-fast local prediction iteration, and rendering the output.

Ensure the environment is properly configured as detailed in the installation guide, then trigger the demonstration orchestrator script (e.g., `python run_demo.py` or the equivalent configured task runner). 

This command isolates the model behavior precisely, allowing developers or presenting researchers to confidently demonstrate the platform's categorization and explainability features instantaneously.
