# ExoIntel

AI-Powered Exoplanet Discovery & Habitability Analytics Platform

## Overview

ExoIntel is a data analytics and artificial intelligence platform designed to analyze exoplanet datasets and identify potentially habitable planets using machine learning and data engineering pipelines.

The platform integrates astronomical datasets, data warehousing, habitability scoring algorithms, and an AI-powered SQL assistant to enable researchers and analysts to explore planetary systems efficiently.

This project demonstrates a full data platform architecture combining data engineering, data science, and AI-assisted analytics.

---

## Core Features

### Exoplanet Data Warehouse

A PostgreSQL-based analytical database storing exoplanetary system data including:

* planetary radius
* planetary mass
* stellar temperature
* equilibrium temperature
* discovery methods
* orbital characteristics

### Habitability Scoring Model

A custom habitability scoring algorithm designed to evaluate how similar a planet is to Earth using parameters such as:

* Earth Similarity Score
* Planetary Density
* Equilibrium Temperature
* Stellar Temperature

The model generates a **Habitability Index** that ranks planets based on potential habitability.

### AI SQL Assistant

An AI-powered natural language interface that converts user questions into SQL queries using a local language model.

Technology used:

* Ollama
* Mistral LLM

Example questions:

* "Show the top 10 most habitable planets"
* "List planets discovered after 2015"
* "Which discovery method found the most planets?"

### Data Engineering Pipeline

Automated ingestion pipeline that:

1. downloads exoplanet datasets
2. transforms raw data
3. loads structured data into PostgreSQL
4. computes analytical features

### Analytical Views

Pre-built SQL analytical views enable fast exploration of planetary data:

* habitability rankings
* discovery trends
* habitability distribution

### Data Visualization

Power BI dashboards can be connected directly to the PostgreSQL warehouse for interactive exploration of exoplanetary datasets.

---

## System Architecture

User Query
↓
AI SQL Assistant (Mistral via Ollama)
↓
SQL Generation
↓
PostgreSQL Data Warehouse
↓
Query Results / Analytics

---

## Tech Stack

Programming Language
Python

Database
PostgreSQL

Machine Learning
Scikit-learn

AI Model
Mistral (via Ollama)

Data Processing
Pandas
NumPy

Visualization
Power BI

Version Control
Git
GitHub

---

## Project Structure

```
exo-intel-platform
│
├── data
│   ├── raw
│   └── processed
│
├── migrations
│
├── src
│   ├── ingestion
│   ├── ml_models
│   ├── ai_assistant
│
├── notebooks
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```
git clone https://github.com/saiiexd/exo-intel-platform.git
```

Install dependencies

```
pip install -r requirements.txt
```

Run database migrations and load the dataset.

---

## Future Improvements

* Advanced machine learning models for habitability prediction
* Interactive analytics interface
* automatic astronomical dataset updates
* AI-powered research assistant for astrophysics queries

---

## Author

Sai Venkat
Engineering Student – Data Science & AI

Project Focus
AI systems
Data Engineering
Machine Learning
