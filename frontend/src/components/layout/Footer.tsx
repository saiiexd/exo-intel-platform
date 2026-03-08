import { useState, useEffect } from 'react';
import apiClient from '@/services/apiClient';

const Footer = () => {
    const [metrics, setMetrics] = useState({ total_visits: 0, active_watchers: 0 });

    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await apiClient.get('/site-metrics');
                setMetrics(response.data);
            } catch (error) {
                console.error('Failed to fetch site metrics:', error);
            }
        };

        fetchMetrics();
        // Set up a polling interval to keep the active watchers feeling "live"
        const interval = setInterval(fetchMetrics, 30000);
        return () => clearInterval(interval);
    }, []);

    return (
        <footer className="mt-auto py-12 px-6 border-t border-white/5 bg-[#030308]">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
                <div className="space-y-4">
                    <div className="flex items-center gap-2">
                        <span className="text-xl font-bold tracking-tight">ExoIntel</span>
                    </div>
                    <p className="text-sm text-muted">
                        The professional AI-driven discovery platform for exoplanetary habitability research.
                    </p>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Platform</h4>
                    <ul className="space-y-2 text-sm text-muted">
                        <li>Discovery Explorer</li>
                        <li>Simulations</li>
                        <li>AI Insights</li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Research</h4>
                    <ul className="space-y-2 text-sm text-muted">
                        <li>Methodology</li>
                        <li>Datasets</li>
                        <li>Documentation</li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Live Traffic</h4>
                    <div className="space-y-3 text-sm">
                        <div className="flex items-center gap-2 text-muted">
                            <span className="w-2 h-2 rounded-full bg-success animate-pulse"></span>
                            <span className="font-mono text-white">{metrics.active_watchers}</span> Active Researchers
                        </div>
                        <div className="flex items-center gap-2 text-muted">
                            <span className="w-2 h-2 rounded-full bg-primary/50"></span>
                            <span className="font-mono text-white">{metrics.total_visits.toLocaleString()}</span> Total Discoveries
                        </div>
                    </div>
                </div>
            </div>

            <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-white/5 flex justify-between items-center text-xs text-muted">
                <p>&copy; 2026 ExoIntel Platform. All rights reserved.</p>
                <p>Scientific Computing & Discovery Architecture</p>
            </div>
        </footer>
    );
};

export default Footer;
