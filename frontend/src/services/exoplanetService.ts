import apiClient from './apiClient';
import { PlanetCandidate } from '../types/planetTypes';

export const exoplanetService = {
    getDiscoveryList: async (): Promise<PlanetCandidate[]> => {
        try {
            const response = await apiClient.get('/top-candidates');
            return response.data;
        } catch (error) {
            console.error('API Error, using fallback data:', error);
            return [
                { name: 'K2-18 b', score: 0.89, dist: 38, status: 'Confirmed' } as any,
                { name: 'Gliese 12 b', score: 0.94, dist: 12, status: 'Candidate' } as any,
                { name: 'Proxima Cen b', score: 0.91, dist: 1.3, status: 'Confirmed' } as any,
                { name: 'TRAPPIST-1 e', score: 0.88, dist: 12.1, status: 'Confirmed' } as any,
                { name: 'Kepler-186 f', score: 0.82, dist: 178, status: 'Confirmed' } as any,
            ];
        }
    },

    getPlanetDetails: async (id: string): Promise<PlanetCandidate | null> => {
        try {
            const response = await apiClient.get(`/planet/${id}`);
            return response.data;
        } catch (error) {
            console.error(`API Error for ${id}, using fallback:`, error);
            return null;
        }
    },

    getDiscoverySummary: async () => {
        try {
            const response = await apiClient.get('/discovery-summary');
            return response.data;
        } catch (error) {
            console.error('API Error for summary, using fallback:', error);
            return { status: "Mock summary data" };
        }
    }
};
