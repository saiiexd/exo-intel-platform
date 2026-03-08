import os
import requests
import pandas as pd
import io
import argparse

TAP_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

# ADQL query for a limited number of records
DEMO_QUERY = """
SELECT TOP {} 
    pl_name, hostname, discoverymethod, disc_year, 
    pl_orbper, pl_rade, pl_masse, pl_dens, pl_eqt,
    st_teff, st_rad, st_mass
FROM pscomppars
"""

COLUMN_MAPPING = {
    "pl_name": "planet_name",
    "hostname": "host_star",
    "discoverymethod": "discovery_method",
    "disc_year": "discovery_year",
    "pl_orbper": "orbital_period",
    "pl_rade": "planet_radius",
    "pl_masse": "planet_mass",
    "pl_dens": "planet_density",
    "pl_eqt": "equilibrium_temperature",
    "st_teff": "stellar_temperature",
    "st_rad": "stellar_radius",
    "st_mass": "stellar_mass"
}

def create_demo_dataset(num_rows=100, output_file="datasets/demo_planets.csv"):
    """
    Fetches a small demonstration dataset natively from the NASA Archive.
    This allows researchers to test the local ML tools without running the full ingestion module.
    """
    print(f"Fetching concise demo dataset ({num_rows} records) from NASA Exoplanet Archive...")
    
    query = DEMO_QUERY.format(num_rows)
    params = {"QUERY": query, "FORMAT": "csv"}
    
    try:
        response = requests.get(TAP_URL, params=params, timeout=30)
        response.raise_for_status()
        
        df = pd.read_csv(io.StringIO(response.text))
        df = df.rename(columns=COLUMN_MAPPING)
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        print(f"Successfully generated demo dataset with {len(df)} records at: {output_file}")
        
    except Exception as e:
        print(f"Failed to fetch demo dataset: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a lightweight ExoIntel demo dataset.")
    parser.add_argument("--rows", type=int, default=100, help="Number of rows to fetch")
    parser.add_argument("--output", type=str, default="datasets/demo_planets.csv", help="Output path for demo file")
    
    args = parser.parse_args()
    create_demo_dataset(args.rows, args.output)
