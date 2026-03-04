CREATE VIEW exoplanet_data.discovery_trends AS
SELECT
    discovery_year,
    discovery_method,
    COUNT(*) AS planets_discovered
FROM exoplanet_data.planets
GROUP BY discovery_year, discovery_method
ORDER BY discovery_year;