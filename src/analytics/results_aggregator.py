"""
results_aggregator.py
======================
Scientific Results Synthesis and Reporting Module.

Aggregates findings from discovery, insights, and explainability layers 
into high-level research summaries and structured datasets in the results/ directory.
"""

import os
import json
import pandas as pd
from datetime import datetime
from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("ResultsAggregator")

def aggregate_results():
    logger.info("Starting Research Results Aggregation...")
    engine = get_engine()
    
    results_data = {
        "report_metadata": {
            "timestamp": datetime.now().isoformat(),
            "platform_version": "v1.3.0-research"
        }
    }
    
    # 1. Aggregate Top Habitable Candidates
    logger.info("Extracting top discovery candidates...")
    candidates_df = pd.DataFrame()
    try:
        candidates_df = pd.read_sql(
            "SELECT planet_name, ml_habitability_score, combined_discovery_score "
            "FROM exoplanet_data.habitable_planet_candidates "
            "ORDER BY combined_discovery_score DESC LIMIT 50",
            engine
        )
        candidates_df.to_csv(os.path.join("results", "top_habitable_candidates.csv"), index=False)
        results_data["discovery_summary"] = {
            "total_candidates_analyzed": len(candidates_df),
            "top_candidate": candidates_df.iloc[0]["planet_name"] if not candidates_df.empty else "N/A"
        }
    except Exception as e:
        logger.warning(f"Could not extract candidates: {e}")

    # 2. Aggregate Feature Importance
    logger.info("Extracting feature importance rankings...")
    importance_df = pd.DataFrame()
    try:
        importance_df = pd.read_sql(
            "SELECT feature_name, mean_abs_shap FROM exoplanet_data.feature_importance_analysis "
            "ORDER BY mean_abs_shap DESC",
            engine
        )
        importance_df.to_csv(os.path.join("results", "feature_importance_ranking.csv"), index=False)
        results_data["scientific_drivers"] = importance_df.head(5).to_dict(orient="records")
    except Exception as e:
        logger.warning(f"Could not extract feature importance: {e}")

    # 3. Population Statistics
    logger.info("Computing population statistics...")
    try:
        stats_df = pd.read_sql(
            "SELECT AVG(ml_habitability_score) as avg_score, COUNT(*) as count "
            "FROM exoplanet_data.habitable_planet_candidates",
            engine
        )
        results_data["population_stats"] = stats_df.to_dict(orient="records")[0]
    except Exception as e:
        logger.warning(f"Could not compute population stats: {e}")

    # 4. Save Aggregated JSON Report
    report_path = os.path.join("results", "research_findings_latest.json")
    with open(report_path, "w") as f:
        json.dump(results_data, f, indent=4)
    
    logger.info(f"Research results successfully aggregated to {report_path}")
    
    # Generate a formal text-based executive summary
    cand_str = candidates_df.head(10).to_string(index=False) if not candidates_df.empty else "No candidates found."
    imp_str = importance_df.head(5).to_string(index=False) if not importance_df.empty else "No feature importance data."
    
    summary_txt = f"""
    ExoIntel Research Results Summary
    ==================================
    Timestamp: {results_data['report_metadata']['timestamp']}
    
    1. Top Discovery Candidates
    ---------------------------
    {cand_str}
    
    2. Primary Scientific Drivers (SHAP)
    ------------------------------------
    {imp_str}
    
    3. Population Analytics
    -----------------------
    Average Habitability Score: {results_data.get('population_stats', {}).get('avg_score', 'N/A')}
    Total Verified Candidates: {results_data.get('population_stats', {}).get('count', 'N/A')}
    """
    
    with open(os.path.join("results", "executive_summary.txt"), "w") as f:
        f.write(summary_txt)

if __name__ == "__main__":
    aggregate_results()
