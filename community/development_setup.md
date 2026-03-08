# Development Setup Guide

This guide details how to set up the ExoIntel environment locally. The project utilizes a Python/FastAPI backend, a React/Vite frontend, and a PostgreSQL data warehouse.

## Prerequisites

Before beginning, ensure you have the following installed:
-   **Python 3.9+**
-   **Node.js 18+** & `npm`
-   **PostgreSQL 14+**
-   **Git**

---

## 1. Database Configuration (PostgreSQL)

1.  Ensure your local PostgreSQL server is running.
2.  Create a specific user and database for the project:
    ```sql
    CREATE DATABASE exoplanet_dw;
    CREATE USER exo_user WITH PASSWORD 'exo_pass123';
    ALTER ROLE exo_user SET client_encoding TO 'utf8';
    ALTER ROLE exo_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE exo_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE exoplanet_dw TO exo_user;
    -- Note: Connect to the database and grant schema usage if required.
    ```
3.  Set up your environment variables. Copy the `.env.example` file to `.env`:
    ```bash
    cp .env.example .env
    ```
    Ensure the `DATABASE_URL` matches your local setup:
    `DATABASE_URL=postgresql://exo_user:exo_pass123@localhost:5432/exoplanet_dw`

---

## 2. Backend Setup (Python / FastAPI)

1.  Navigate to the repository root.
2.  Create and activate a virtual environment:
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. *Optional: Run the pipeline to populate your local database.* If you want to fetch live NASA data and run the ML models:
    ```bash
    python run_exointel_pipeline.py --run-all
    ```
5.  Start the FastAPI backend server:
    ```bash
    python -m src.api.main
    ```
    The API will be accessible at `http://localhost:8000`.

---

## 3. Frontend Setup (React / Vite)

The interactive discovery explorer is built with React, TypeScript, and Vite.

1.  Open a new terminal window and navigate to the `frontend/` directory:
    ```bash
    cd frontend
    ```
2.  Install Node dependencies:
    ```bash
    npm install
    ```
3.  Start the Vite development server:
    ```bash
    npm run dev
    ```
    The web interface will be accessible at `http://localhost:5173`.

---

## 4. Research Dashboard Setup (Streamlit)

For internal data science exploration, the platform also includes a Streamlit dashboard.

1. Ensure your Python virtual environment is activated.
2. Run the Streamlit app:
    ```bash
    streamlit run src/frontend/app.py
    ```
    The dashboard will be available at `http://localhost:8501`.
