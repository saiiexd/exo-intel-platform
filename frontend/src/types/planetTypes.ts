export interface PlanetCandidate {
    id: string;
    name: string;
    discovery_method: string;
    discovery_year: number;
    distance_pc: number;
    habitability_score: number;
    status: 'Confirmed' | 'Candidate' | 'False Positive';
    orbital_period_days: number;
    planet_radius_earth: number;
    planet_mass_earth: number;
    equilibrium_temp_k: number;
    stellar_name: string;
    stellar_type: string;
    stellar_temp_k: number;
}

export interface HabitabilityPrediction {
    planet_id: string;
    predicted_score: number;
    confidence_interval: [number, number];
    model_version: string;
    timestamp: string;
    shap_values: Record<string, number>;
}

export interface DiscoveryMetrics {
    total_planets_analyzed: number;
    habitable_candidates_found: number;
    model_average_precision: number;
    last_pipeline_run: string;
}
