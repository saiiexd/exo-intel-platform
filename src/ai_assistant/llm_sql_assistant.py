import pandas as pd
from prompt_toolkit import output
from sqlalchemy import create_engine
import ollama
from utils.db import get_engine


# PostgreSQL connection
engine = get_engine()


# Database schema provided to the LLM
schema_description = """
Database schema:

Table: exoplanet_data.planets
Columns:
planet_id
planet_name
discovery_year
planet_radius
planet_mass
planet_density
equilibrium_temperature
stellar_temperature
stellar_mass
stellar_radius
earth_similarity_score
habitability_index
habitable_zone

Views:
exoplanet_data.discovery_trends
exoplanet_data.habitability_analysis
exoplanet_data.habitability_ranking
exoplanet_data.habitability_distribution
"""


def generate_sql(question):

    prompt = f"""
You are a PostgreSQL expert.

Convert the following question into SQL.

Return ONLY the SQL query. No explanation.

Schema:
{schema_description}

Question:
{question}
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    output = response["message"]["content"]

    # Remove markdown blocks if present
    if "```" in output:
        parts = output.split("```")
        for part in parts:
            if "select" in part.lower():
                output = part
                break

    # Extract only SQL starting from SELECT
    lower = output.lower()
    if "select" in lower:
        output = output[lower.index("select"):]

    # Remove trailing explanation after SQL
    # Remove MySQL backticks
    output = output.replace("`", "")

    # Fix common column hallucinations
    output = output.replace("habitatability_index", "habitability_index")
    output = output.replace("habitability_score", "habitability_index")

    return output.strip()


def run_query(sql):

    df = pd.read_sql(sql, engine)

    print("\nGenerated SQL:\n")
    print(sql)

    print("\nQuery Result:\n")
    print(df.head(20))


if __name__ == "__main__":

    while True:

        question = input("\nAsk ExoIntel AI: ")

        if question.lower() == "exit":
            break

        try:
            sql = generate_sql(question)
            run_query(sql)
        except Exception as e:
            print("\nError:", e)