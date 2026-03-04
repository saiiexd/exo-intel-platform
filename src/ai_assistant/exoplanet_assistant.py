import pandas as pd
from utils.db import get_psycopg2_conn


conn = get_psycopg2_conn()


def run_query(sql):
    df = pd.read_sql(sql, conn)
    print(df)


def assistant(question):

    question = question.lower()

    if "top habitable planets" in question:

        sql = """
        SELECT planet_name, habitability_index
        FROM exoplanet_data.habitability_ranking
        LIMIT 10;
        """

        run_query(sql)

    elif "planets discovered after" in question:

        year = int(question.split("after")[1].strip())

        sql = f"""
        SELECT planet_name, discovery_year, habitability_index
        FROM exoplanet_data.habitability_ranking
        WHERE discovery_year > {year}
        ORDER BY habitability_index DESC
        LIMIT 10;
        """

        run_query(sql)

    elif "habitability distribution" in question:

        sql = """
        SELECT *
        FROM exoplanet_data.habitability_distribution;
        """

        run_query(sql)

    else:
        print("Query not recognized.")


while True:

    q = input("\nAsk ExoIntel: ")

    if q == "exit":
        break

    assistant(q)