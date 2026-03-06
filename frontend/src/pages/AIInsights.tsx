import { BarChart3, PieChart, Activity } from 'lucide-react';
import ChartContainer from '@/components/ui/ChartContainer';

const AIInsights = () => {
    return (
        <div className="space-y-8">
            <header>
                <h1 className="text-3xl font-bold">AI Insights</h1>
                <p className="text-muted">Detailed analysis of model behavior, feature importance, and astrophysical correlations.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <ChartContainer
                    title="Global Feature Importance (SHAP)"
                    icon={<BarChart3 className="w-4 h-4 text-primary" />}
                    description="Relative impact of planetary parameters on the habitability consensus score across the entire NASA dataset."
                >
                    [Interactive SHAP Bar Chart Placeholder]
                </ChartContainer>

                <ChartContainer
                    title="Correlation Analysis: Discovery Method"
                    icon={<PieChart className="w-4 h-4 text-secondary" />}
                    description="Analyzing whether specific discovery methods (Transit, Radial Velocity) introduce bias in habitability predictions."
                >
                    [Discovery Method vs Habitability Chart Placeholder]
                </ChartContainer>

                <div className="md:col-span-2">
                    <ChartContainer
                        title="Model Confidence & Error Distribution"
                        icon={<Activity className="w-4 h-4 text-success" />}
                        description="Monitoring the statistical variance of the habitability index across planetary clusters."
                    >
                        <div className="h-48 flex items-center justify-center">
                            [Error Metrics / Loss Distribution Chart Placeholder]
                        </div>
                    </ChartContainer>
                </div>
            </div>
        </div>
    );
};

export default AIInsights;
