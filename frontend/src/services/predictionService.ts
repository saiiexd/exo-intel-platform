import apiClient from './apiClient';
import { HabitabilityPrediction } from '../types/planetTypes';

export const predictionService = {
    predictHabitability: async (params: any): Promise<HabitabilityPrediction | null> => {
        try {
            // Note: Currently no prediction endpoint in main.py, providing mock behavior
            console.log('Simulating habitability prediction:', params);
            return {
                score: 0.85,
                confidence: 0.92
            } as any;
        } catch (error) {
            return null;
        }
    },

    getGlobalFeatureImportance: async () => {
        try {
            const response = await apiClient.get('/feature-importance');
            return response.data;
        } catch (error) {
            console.error('API Error, using fallback:', error);
            return [{ feature: 'mock_feature', mean_abs_shap: 0.1 }];
        }
    }
};
