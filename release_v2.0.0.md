# ExoIntel Platform v2.0.0 - Stable Open-Source Release

We are incredibly excited to announce the **stable v2.0.0 release** of the **ExoIntel AI Exoplanet Discovery Platform**. This release marks the transition of ExoIntel from an internal research tool into a comprehensive, community-ready scientific architecture designed for astrophysics and machine learning researchers.

ExoIntel bridges the gap between raw astronomical surveys and interpretable discovery by providing an automated, scalable pipeline that ranks candidate planets for habitability based on physical constraints and ML intelligence.

## 🌟 Key Capabilities in v2.0.0

### **1. AI Discovery Engine**
At the heart of ExoIntel is a robust machine learning ranking engine utilizing high-performance Gradient Boosting models. By cross-referencing engineered astrophysical features against the Earth Similarity Index (ESI) and stellar flux calculations, the engine autonomously processes thousands of planetary candidates and prioritizes high-confidence habitable targets.

### **2. Explainable AI (XAI) Integration**
"Black box" intelligence is no longer sufficient for scientific inquiry. ExoIntel v2.0.0 integrates rigorous **SHAP (SHapley Additive exPlanations)** analysis natively into its workflow. For every prediction, the platform generates granular waterfall and summary plots, breaking down exactly how parameters like Equilibrium Temperature or Planet Radius influenced the algorithm's final consensus. 

### **3. Automated Pipeline Orchestration**
Research reproducibility is fundamentally solved through our "Scientific-as-Code" framework. A single python command (`python run_exointel_pipeline.py`) orchestrates the entire continuous workflow: fetching the latest live data from the NASA archive, running data transformations, training the ML model, running inference, drawing SHAP insights, and issuing final scientific reports.

### **4. Interactive Research Interfaces**
To democratize data access, v2.0.0 ships with dual visualization layers:
- **Streamlit Research Dashboard**: A python-native analytical backend specifically structured for rapid prototyping and live algorithmic comparisons.
- **Interactive React Frontend**: A polished, modern web application providing the research community with deep-dive planet profiles, live ML habitability simulations, and discovery leaderboards.

## 📁 Repository Updates for Open-Source
- Introduced comprehensive `CITATION.cff`, `CONTRIBUTING.md`, and `CODE_OF_CONDUCT.md` templates.
- Added graceful offline-fallback demonstrations, meaning researchers can spin up the frontends instantly without needing a localized PostgreSQL data warehouse initialized.
- Cleaned and organized the repository structure into dedicated `science/`, `community/`, and `analysis_outputs/` zones.

Thank you to our community for the ongoing collaboration. Dive into the repository and happy discovering!
