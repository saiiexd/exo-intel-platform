CREATE VIEW exoplanet_data.habitability_ranking AS
SELECT
    planet_name,
    discovery_year,
    stellar_temperature,
    planet_radius,
    planet_mass,
    equilibrium_temperature,
    habitability_index
FROM exoplanet_data.planets
WHERE habitability_index IS NOT NULL
ORDER BY habitability_index DESC;