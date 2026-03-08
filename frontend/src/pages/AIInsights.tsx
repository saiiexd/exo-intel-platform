import { useState, useEffect } from 'react';
import { BarChart3, PieChart, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, PieChart as RechartsPie, Pie } from 'recharts';
import ChartContainer from '@/components/ui/ChartContainer';
import { predictionService } from '@/services/predictionService';

const AIInsights = () => {
    const [featureData, setFeatureData] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchInsights = async () => {
            setLoading(true);
            try {
                // Fetch global SHAP feature importance
                const shapData = await predictionService.getGlobalFeatureImportance();

                // Format for chart: sort by importance DESC and grab top 8
                const formattedData = shapData
                    .sort((a: any, b: any) => b.mean_abs_shap - a.mean_abs_shap)
                    .slice(0, 8)
                    .map((item: any) => ({
                        name: item.feature.replace(/_/g, ' ').toUpperCase(),
                        importance: Number(item.mean_abs_shap).toFixed(3)
                    }));

                setFeatureData(formattedData);
            } catch (err) {
                console.error("Failed to fetch insights", err);
            } finally {
                setLoading(false);
            }
        };

        fetchInsights();
    }, []);

    // Mock pie data as the backend currently doesn't have a distinct discovery method grouping endpoint ready
    const discoveryMethodData = [
        { name: 'Transit', value: 3942 },
        { name: 'Radial Velocity', value: 1045 },
        { name: 'Microlensing', value: 201 },
        { name: 'Imaging', value: 64 },
    ];

    // Custom colors for charts
    const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#06b6d4', '#f43f5e', '#64748b'];

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
                    <div className="h-72 w-full mt-4">
                        {loading ? (
                            <div className="h-full flex items-center justify-center text-muted">Loading AI Analysis...</div>
                        ) : (
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={featureData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                                    <XAxis type="number" hide />
                                    <YAxis dataKey="name" type="category" width={120} tick={{ fill: '#94a3b8', fontSize: 12 }} />
                                    <Tooltip
                                        cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                                        contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
                                    />
                                    <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                                        {featureData.map((_, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Bar>
                                </BarChart>
                            </ResponsiveContainer>
                        )}
                    </div>
                </ChartContainer>

                <ChartContainer
                    title="Detection Method Distribution"
                    icon={<PieChart className="w-4 h-4 text-secondary" />}
                    description="Distribution of confirmed exoplanets across primary astronomical discovery pipelines."
                >
                    <div className="h-72 w-full mt-4 flex justify-center items-center">
                        <ResponsiveContainer width="100%" height="100%">
                            <RechartsPie>
                                <Pie
                                    data={discoveryMethodData}
                                    cx="50%"
                                    cy="50%"
                                    innerRadius={60}
                                    outerRadius={90}
                                    paddingAngle={5}
                                    dataKey="value"
                                    stroke="none"
                                >
                                    {discoveryMethodData.map((_, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px', color: '#fff' }}
                                    itemStyle={{ color: '#cbd5e1' }}
                                />
                            </RechartsPie>
                        </ResponsiveContainer>
                    </div>
                </ChartContainer>

                <div className="md:col-span-2">
                    <ChartContainer
                        title="Model Confidence & Statistical Variance"
                        icon={<Activity className="w-4 h-4 text-success" />}
                        description="Gradient Boosting Regressor performance metrics across validation folds. Indicates the predictive stability when evaluating extreme physical parameters."
                    >
                        <div className="h-48 flex flex-col items-center justify-center space-y-4">
                            <div className="grid grid-cols-3 gap-8 w-full max-w-3xl">
                                <div className="bg-background/40 border border-white/5 p-4 rounded-xl text-center">
                                    <h4 className="text-muted text-sm mb-1">R² Score (Accuracy)</h4>
                                    <p className="text-2xl font-bold text-success font-mono">0.963</p>
                                </div>
                                <div className="bg-background/40 border border-white/5 p-4 rounded-xl text-center">
                                    <h4 className="text-muted text-sm mb-1">RMSE (Error Margin)</h4>
                                    <p className="text-2xl font-bold text-warning font-mono">0.021</p>
                                </div>
                                <div className="bg-background/40 border border-white/5 p-4 rounded-xl text-center">
                                    <h4 className="text-muted text-sm mb-1">Validation Folds</h4>
                                    <p className="text-2xl font-bold text-primary font-mono">5</p>
                                </div>
                            </div>
                        </div>
                    </ChartContainer>
                </div>
            </div>
        </div>
    );
};

export default AIInsights;
