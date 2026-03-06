import { useState } from 'react';
import { HabitabilityPrediction } from '../types/planetTypes';
import { predictionService } from '../services/predictionService';

export const useHabitabilityPrediction = () => {
    const [prediction, setPrediction] = useState<HabitabilityPrediction | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const predict = async (params: any) => {
        try {
            setLoading(true);
            const data = await predictionService.predictHabitability(params);
            setPrediction(data);
        } catch (err: any) {
            setError(err.message || 'Prediction failed');
        } finally {
            setLoading(false);
        }
    };

    return { predict, prediction, loading, error };
};
