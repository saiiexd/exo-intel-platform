import apiClient from './apiClient';
import { HabitabilityPrediction } from '../types/planetTypes';

export const predictionService = {
    predictHabitability: async (params: any): Promise<HabitabilityPrediction | null> => {
        console.log('Running habitability prediction with params:', params);
        return null;
    },

    getGlobalFeatureImportance: async () => {
        console.log('Fetching global feature importance...');
        return null;
    }
};
