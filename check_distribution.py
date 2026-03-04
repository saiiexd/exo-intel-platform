import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql://postgres:saivenkat143@localhost:5432/exo_intel_db")

query = """
SELECT habitability_index
FROM exoplanet_data.habitability_ranking
"""

df = pd.read_sql(query, engine)

print("Average habitability:", df["habitability_index"].mean())
print("Min:", df["habitability_index"].min())
print("Max:", df["habitability_index"].max())