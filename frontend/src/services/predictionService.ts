import apiClient from './apiClient';
import { HabitabilityPrediction } from '../types/planetTypes';

export const predictionService = {
    predictHabitability: async (params: any): Promise<HabitabilityPrediction | null> => {
        try {
            const response = await apiClient.post('/predict', params);
            return response.data;
        } catch (error) {
            console.error('API Error during habitability prediction:', error);
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
