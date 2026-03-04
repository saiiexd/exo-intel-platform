from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sqlalchemy import create_engine
import ollama
from fastapi.middleware.cors import CORSMiddleware
from utils.db import get_engine

app = FastAPI()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = get_engine()

schema_description = """
Table: exoplanet_data.planets
Columns:
planet_name
discovery_year
planet_radius
planet_mass
planet_density
equilibrium_temperature
stellar_temperature
earth_similarity_score
habitability_index
"""


class Query(BaseModel):
    question: str


def generate_sql(question):

    prompt = f"""
Convert this question to PostgreSQL SQL.

Schema:
{schema_description}

Question:
{question}

Return only SQL.
"""

    response = ollama.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )

    sql = response["message"]["content"]

    if "select" in sql.lower():
        sql = sql[sql.lower().index("select"):]

    sql = sql.replace("`", "")

    if ";" in sql:
        sql = sql.split(";")[0] + ";"

    return sql


@app.post("/ask")
def ask_ai(query: Query):

    sql = generate_sql(query.question)

    df = pd.read_sql(sql, engine)

    return {
        "sql": sql,
        "data": df.head(20).to_dict(orient="records")
    }