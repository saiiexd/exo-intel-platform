import { PlanetCandidate } from './planetTypes';

export interface DiscoveryBatch {
    batch_id: string;
    timestamp: string;
    candidates_count: number;
    top_candidate: PlanetCandidate;
}

export interface ResearchScenario {
    id: string;
    title: string;
    description: string;
    parameters: Record<string, number>;
}

export interface SystemStatus {
    database_ready: boolean;
    ml_model_loaded: boolean;
    api_connected: boolean;
    last_sync: string;
}
