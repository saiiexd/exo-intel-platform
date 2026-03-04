-- Add planet density column
ALTER TABLE exoplanet_data.planets
ADD COLUMN planet_density FLOAT;

-- Compute density from mass and radius
UPDATE exoplanet_data.planets
SET planet_density = planet_mass / POWER(planet_radius,3)
WHERE planet_mass IS NOT NULL
AND planet_radius IS NOT NULL;

-- Add habitable zone classification
ALTER TABLE exoplanet_data.planets
ADD COLUMN habitable_zone VARCHAR(20);

-- Populate habitable zone labels
UPDATE exoplanet_data.planets
SET habitable_zone =
CASE
    WHEN equilibrium_temperature BETWEEN 180 AND 303 THEN 'potential_habitable'
    WHEN equilibrium_temperature < 180 THEN 'too_cold'
    WHEN equilibrium_temperature > 303 THEN 'too_hot'
END;