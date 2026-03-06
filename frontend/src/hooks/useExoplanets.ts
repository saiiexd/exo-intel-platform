import { useState, useEffect } from 'react';
import { PlanetCandidate } from '../types/planetTypes';
import { exoplanetService } from '../services/exoplanetService';

export const useExoplanets = () => {
    const [planets, setPlanets] = useState<PlanetCandidate[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchPlanets = async () => {
            try {
                setLoading(true);
                const data = await exoplanetService.getDiscoveryList();
                setPlanets(data);
            } catch (err: any) {
                setError(err.message || 'Failed to fetch planets');
            } finally {
                setLoading(false);
            }
        };

        fetchPlanets();
    }, []);

    return { planets, loading, error };
};
