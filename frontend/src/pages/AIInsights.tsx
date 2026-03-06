import { BarChart3, PieChart, Activity } from 'lucide-react';

const AIInsights = () => {
    return (
        <div className="space-y-8">
            <header>
                <h1 className="text-3xl font-bold">AI Insights</h1>
                <p className="text-muted">Detailed analysis of model behavior, feature importance, and astrophysical correlations.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                {/* Global Feature Importance */}
                <section className="cosmic-card p-6 space-y-6">
                    <div className="flex items-center justify-between">
                        <h3 className="font-bold flex items-center gap-2 text-sm">
                            <BarChart3 className="w-4 h-4 text-primary" />
                            Global Feature Importance (SHAP)
                        </h3>
                    </div>
                    <div className="h-64 flex items-center justify-center text-muted italic border border-white/5 rounded-lg bg-[#030308]">
                        [Interactive SHAP Bar Chart Placeholder]
                    </div>
                    <p className="text-xs text-muted">
                        Relative impact of planetary parameters on the habitability consensus score across the entire NASA dataset.
                    </p>
                </section>

                {/* Discovery Methodology Correlation */}
                <section className="cosmic-card p-6 space-y-6">
                    <div className="flex items-center justify-between">
                        <h3 className="font-bold flex items-center gap-2 text-sm">
                            <PieChart className="w-4 h-4 text-secondary" />
                            Correlation Analysis: Discovery Method
                        </h3>
                    </div>
                    <div className="h-64 flex items-center justify-center text-muted italic border border-white/5 rounded-lg bg-[#030308]">
                        [Discovery Method vs Habitability Chart Placeholder]
                    </div>
                    <p className="text-xs text-muted">
                        Analyzing whether specific discovery methods (Transit, Radial Velocity) introduce bias in habitability predictions.
                    </p>
                </section>

                {/* Prediction Confidence Distribution */}
                <section className="md:col-span-2 cosmic-card p-6 space-y-6">
                    <div className="flex items-center justify-between">
                        <h3 className="font-bold flex items-center gap-2 text-sm">
                            <Activity className="w-4 h-4 text-success" />
                            Model Confidence & Error Distribution
                        </h3>
                    </div>
                    <div className="h-48 flex items-center justify-center text-muted italic border border-white/5 rounded-lg bg-[#030308]">
                        [Error Metrics / Loss Distribution Chart Placeholder]
                    </div>
                    <p className="text-xs text-muted">
                        Monitoring the statistical variance of the habitability index across planetary clusters.
                    </p>
                </section>
            </div>
        </div>
    );
};

export default AIInsights;
