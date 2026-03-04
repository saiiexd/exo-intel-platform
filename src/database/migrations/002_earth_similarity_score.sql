ALTER TABLE exoplanet_data.planets
ADD COLUMN earth_similarity_score FLOAT;

UPDATE exoplanet_data.planets
SET earth_similarity_score =
(
    (1 - ABS(planet_radius - 1) / 1) +
    (1 - ABS(planet_mass - 1) / 1) +
    (1 - ABS(equilibrium_temperature - 255) / 255)
) / 3
WHERE planet_radius IS NOT NULL
AND planet_mass IS NOT NULL
AND equilibrium_temperature IS NOT NULL;