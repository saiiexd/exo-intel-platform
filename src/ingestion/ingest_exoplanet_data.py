import requests
from utils.db import get_psycopg2_conn

# NASA dataset API
url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query=select+pl_name,hostname,discoverymethod,disc_year,pl_orbper,pl_rade,pl_bmasse,pl_eqt,st_teff,st_mass,st_rad+from+pscomppars&format=json"

print("Downloading dataset from NASA...")

response = requests.get(url)
data = response.json()

print("Records received:", len(data))


# PostgreSQL connection
conn = get_psycopg2_conn()

cursor = conn.cursor()

print("Connected to PostgreSQL")


# Insert query
insert_query = """
INSERT INTO exoplanet_data.planets
(planet_name, host_star, discovery_method, discovery_year,
orbital_period, planet_radius, planet_mass, equilibrium_temperature,
stellar_temperature, stellar_mass, stellar_radius)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""


insert_count = 0

for planet in data:

    values = (
        planet.get("pl_name"),
        planet.get("hostname"),
        planet.get("discoverymethod"),
        planet.get("disc_year"),
        planet.get("pl_orbper"),
        planet.get("pl_rade"),
        planet.get("pl_bmasse"),
        planet.get("pl_eqt"),
        planet.get("st_teff"),
        planet.get("st_mass"),
        planet.get("st_rad")
    )

    try:
        cursor.execute(insert_query, values)
        insert_count += 1
    except:
        pass


conn.commit()

print("Inserted records:", insert_count)

cursor.close()
conn.close()

print("Pipeline completed")