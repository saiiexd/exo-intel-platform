CREATE VIEW exoplanet_data.habitability_analysis AS
SELECT
    planet_name,
    discovery_year,
    planet_radius,
    planet_mass,
    planet_density,
    equilibrium_temperature,
    stellar_temperature,
    earth_similarity_score,
    habitable_zone
FROM exoplanet_data.planets
WHERE earth_similarity_score IS NOT NULL;