"""
discovery_summary_generator.py
==============================
Generates a human-readable discovery summary report (discovery_summary.txt)
based on the latest results in the PostgreSQL database.
"""

import os
import pandas as pd
from src.config.config import config
from src.utils.logger import setup_logger
from src.utils.db import get_engine

logger = setup_logger("SummaryGenerator")

def generate_discovery_summary():
    logger.info("Generating Discovery Summary report...")
    engine = get_engine()
    
    try:
        # 1. Fetch metrics
        total_enriched = pd.read_sql("SELECT COUNT(*) FROM exoplanet_data.planets_enriched", engine).iloc[0, 0]
        df_candidates = pd.read_sql("SELECT * FROM exoplanet_data.habitable_planet_candidates", engine)
        
        total_candidates = len(df_candidates)
        max_ml_score = df_candidates['ml_habitability_score'].max() if not df_candidates.empty else 0.0
        
        # 2. Multi-planet high-habitability systems
        # We'll define "high habitability" as score > 0.7 for summary purposes
        high_hab_threshold = 0.7
        high_hab_planets = df_candidates[df_candidates['ml_habitability_score'] >= high_hab_threshold]
        
        # We need the host star. In habitable_planet_candidates we might not have it directly, 
        # let's check the schema or join with planets_enriched if needed.
        # Wait, many candidates might share a host star.
        
        # Let's join to get host star if not present
        if 'host_star' not in df_candidates.columns:
            df_enriched = pd.read_sql("SELECT planet_name, host_star FROM exoplanet_data.planets_enriched", engine)
            df_candidates = pd.merge(df_candidates, df_enriched, on="planet_name", how="left")
            high_hab_planets = df_candidates[df_candidates['ml_habitability_score'] >= high_hab_threshold]
        
        system_counts = high_hab_planets.groupby("host_star").size().reset_index(name="hab_count")
        multi_planet_systems = system_counts[system_counts["hab_count"] > 1]
        num_multi_systems = len(multi_planet_systems)
        
        # 3. Top Candidate
        top_candidate = "None"
        top_score = 0.0
        if not df_candidates.empty:
            best_idx = df_candidates['combined_discovery_score'].idxmax()
            top_candidate = df_candidates.loc[best_idx, 'planet_name']
            top_score = df_candidates.loc[best_idx, 'combined_discovery_score']

        # 4. Generate Report
        report_path = os.path.join(config.OUTPUT_DIR, "discovery_summary.txt")
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        with open(report_path, "w") as f:
            f.write("============================================================\n")
            f.write("      ExoIntel – Autonomous AI Discovery Summary\n")
            f.write("============================================================\n\n")
            f.write(f"Total Planets Processed:   {total_enriched:,}\n")
            f.write(f"Habitable Candidates:      {total_candidates:,}\n")
            f.write(f"Highest ML Score:          {max_ml_score:.4f}\n")
            f.write(f"Multi-Planet Hab. Systems: {num_multi_systems}\n\n")
            f.write("------------------------------------------------------------\n")
            f.write("🏆 TOP DISCOVERY CANDIDATE\n")
            f.write("------------------------------------------------------------\n")
            f.write(f"Name:            {top_candidate}\n")
            f.write(f"Discovery Score: {top_score:.4f}\n\n")
            f.write("DISCOVERY LOG:\n")
            f.write(f"The ExoIntel pipeline has successfully analyzed {total_enriched} planetary systems.\n")
            f.write(f"Out of these, {total_candidates} have been identified as high-priority candidates.\n")
            if num_multi_systems > 0:
                f.write(f"Notably, {num_multi_systems} star systems host multiple potentially habitable planets.\n")
            f.write(f"The leading candidate for future observation is {top_candidate}.\n\n")
            f.write("------------------------------------------------------------\n")
            f.write("Generated automatically by ExoIntel Pipeline Orchestrator.\n")
            f.write("============================================================\n")
            
        logger.info(f"Discovery summary report saved to {report_path}")
        
    except Exception as e:
        logger.error(f"Failed to generate discovery summary: {e}")

if __name__ == "__main__":
    generate_discovery_summary()
