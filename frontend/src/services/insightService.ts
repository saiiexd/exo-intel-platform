import apiClient from './apiClient';

export const insightService = {
    getPipelineMetrics: async () => {
        try {
            const response = await apiClient.get('/metrics/pipeline');
            return response.data;
        } catch (error) {
            console.error('API Error for pipeline metrics:', error);
            return [];
        }
    },
    getModelMetrics: async () => {
        try {
            const response = await apiClient.get('/metrics/model');
            return response.data;
        } catch (error) {
            console.error('API Error for model metrics:', error);
            return null;
        }
    },
    getDiscoveryMetrics: async () => {
        try {
            const response = await apiClient.get('/metrics/discovery');
            return response.data;
        } catch (error) {
            console.error('API Error for discovery metrics:', error);
            return [];
        }
    }
};
