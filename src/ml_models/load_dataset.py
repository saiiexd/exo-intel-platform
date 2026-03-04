import psycopg2
import pandas as pd

# Database connection
conn = psycopg2.connect(
    host="localhost",
    database="exo_intel_db",
    user="postgres",
    password="saivenkat143"
)

query = """
SELECT 
planet_name,
orbital_period,
planet_radius,
planet_mass,
equilibrium_temperature,
stellar_temperature,
stellar_mass,
stellar_radius,
planet_density,
earth_similarity_score,
habitable_zone
FROM exoplanet_data.planets
WHERE earth_similarity_score IS NOT NULL
"""

df = pd.read_sql(query, conn)

conn.close()

print("Dataset loaded")
print("Rows:", len(df))
print(df.head())