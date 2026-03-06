import apiClient from './apiClient';
import { PlanetCandidate } from '../types/planetTypes';

export const exoplanetService = {
    getDiscoveryList: async (): Promise<PlanetCandidate[]> => {
        // Placeholder for future API call
        console.log('Fetching discovery list...');
        return [];
    },

    getPlanetDetails: async (id: string): Promise<PlanetCandidate | null> => {
        console.log(`Fetching details for ${id}...`);
        return null;
    },

    getDiscoverySummary: async () => {
        console.log('Fetching discovery summary...');
        return null;
    }
};
