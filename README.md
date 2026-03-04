# ExoIntel – AI Platform for Exoplanet Habitability Analysis

## Overview

ExoIntel is a data science platform designed to analyze exoplanet datasets and estimate planetary habitability using machine learning.

The system integrates data engineering, analytics, and machine learning to explore potential Earth-like planets discovered in astronomical surveys.

This project demonstrates how modern data platforms can combine databases, machine learning models, and interactive dashboards to analyze astrophysical datasets.

---

## Key Features

**Data Warehouse**

A PostgreSQL database stores exoplanet data and derived analytics tables.

**SQL Analytics Layer**

Custom SQL views compute aggregated statistics and habitability ranking metrics.

**Machine Learning Model**

A Random Forest regression model predicts a habitability score based on planetary and stellar parameters.

**Power BI Dashboard**

An interactive analytics dashboard provides insights into planet distributions, stellar systems, and predicted habitability.

**Interactive Web Application**

A Streamlit application allows users to explore planets and simulate habitability predictions using adjustable astrophysical parameters.

---

## Technology Stack

Python
PostgreSQL
SQLAlchemy
Scikit-learn
Streamlit
Plotly
Power BI

---

## Project Architecture

Data Flow

Database (PostgreSQL)
↓
SQL Views & Data Preparation
↓
Machine Learning Model
↓
Interactive Analytics (Power BI + Streamlit)

---

## Machine Learning Model

The habitability model analyzes the following planetary and stellar parameters:

* Planet Radius
* Planet Mass
* Planet Density
* Equilibrium Temperature
* Stellar Temperature
* Stellar Mass
* Stellar Radius

The model predicts a habitability score representing the likelihood that a planet could support Earth-like conditions.

---

## Running the Project

### 1 Install Dependencies

```
pip install -r requirements.txt
```

### 2 Train the Model

```
python src/ml_models/train_habitability_model.py
```

### 3 Launch the Web Application

```
streamlit run src/frontend/app.py
```

---

## Example Use Cases

Exploring Earth-like planets in exoplanet datasets
Understanding relationships between stellar and planetary properties
Simulating hypothetical planetary systems
Demonstrating end-to-end data science pipelines

---

## Future Improvements

Improved feature engineering for habitability modeling
Automated discovery of potentially habitable planets
Advanced model interpretability techniques
Expanded astrophysical datasets

---

## Author

Sai Venkat
Engineering Student – Data Science & Machine Learning
