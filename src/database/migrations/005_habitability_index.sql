ALTER TABLE exoplanet_data.planets
ADD COLUMN habitability_index FLOAT;

UPDATE exoplanet_data.planets
SET habitability_index =
(
    COALESCE(earth_similarity_score,0) * 0.4 +
    COALESCE(planet_density,0) * 0.2 +
    (1 - ABS(equilibrium_temperature - 255)/255) * 0.2 +
    (1 - ABS(stellar_temperature - 5778)/5778) * 0.2
)
WHERE earth_similarity_score IS NOT NULL;