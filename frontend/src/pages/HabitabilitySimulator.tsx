import { useState } from 'react';
import { Sliders, Play, Info } from 'lucide-react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { useHabitabilityPrediction } from '../hooks/useHabitabilityPrediction';

const HabitabilitySimulator = () => {
    const { predict, prediction, loading } = useHabitabilityPrediction();

    const [params, setParams] = useState({
        radius: 1.0,
        mass: 1.0,
        temp: 288,
        axis: 1.0,
        lum: 1.0
    });

    const handleParamChange = (key: keyof typeof params, value: number) => {
        setParams(prev => ({ ...prev, [key]: value }));
    };

    const handleRunPrediction = () => {
        predict(params);
    };

    const controls = [
        { key: 'radius', label: 'Planet Radius (Earth Radii)', min: 0.1, max: 2.5, val: params.radius },
        { key: 'mass', label: 'Planet Mass (Earth Masses)', min: 0.1, max: 10.0, val: params.mass },
        { key: 'temp', label: 'Effective Temperature (K)', min: 50, max: 2000, val: params.temp },
        { key: 'axis', label: 'Orbital Semimajor Axis (AU)', min: 0.01, max: 50.0, val: params.axis },
        { key: 'lum', label: 'Stellar Luminosity (Solar)', min: 0.001, max: 100.0, val: params.lum },
    ];

    const predictedScore = prediction ? ((prediction as any).score ?? prediction.predicted_score ?? 0) : null;

    return (
        <div className="space-y-8">
            <header>
                <h1 className="text-3xl font-bold">Habitability Simulator</h1>
                <p className="text-muted">Test planetary parameters against the ExoIntel ML models to predict habitability.</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Controls Panel */}
                <section>
                    <Card className="p-8 space-y-8">
                        <div className="flex items-center justify-between">
                            <h3 className="font-bold flex items-center gap-2">
                                <Sliders className="w-4 h-4 text-primary" />
                                Planetary Parameters
                            </h3>
                            <button
                                onClick={() => setParams({ radius: 1.0, mass: 1.0, temp: 288, axis: 1.0, lum: 1.0 })}
                                className="text-xs text-primary hover:underline"
                            >
                                Reset to Earth-Standard
                            </button>
                        </div>

                        <div className="grid gap-6">
                            {controls.map((param, idx) => (
                                <div key={idx} className="space-y-3">
                                    <div className="flex justify-between text-xs font-medium">
                                        <label className="text-muted">{param.label}</label>
                                        <span className="text-primary font-mono">{param.val.toFixed(2)}</span>
                                    </div>
                                    <input
                                        type="range"
                                        min={param.min}
                                        max={param.max}
                                        step={(param.max - param.min) / 100}
                                        value={param.val}
                                        onChange={(e) => handleParamChange(param.key as any, parseFloat(e.target.value))}
                                        className="w-full accent-primary bg-white/5 h-1.5 rounded-full appearance-none outline-none"
                                    />
                                </div>
                            ))}
                        </div>

                        <Button
                            className="w-full gap-2"
                            size="lg"
                            onClick={handleRunPrediction}
                            disabled={loading}
                        >
                            <Play className="w-4 h-4 fill-current" />
                            {loading ? 'Predicting...' : 'Run Prediction Model'}
                        </Button>
                    </Card>
                </section>

                {/* Prediction Output Section */}
                <div className="space-y-8">
                    <section className="h-full">
                        <Card className="p-8 flex flex-col items-center justify-center text-center h-full">
                            <div className="space-y-2 mb-8">
                                <h3 className="text-sm font-bold uppercase tracking-widest text-muted">Habitability Index</h3>
                                <div className={`text-6xl font-bold transition-colors ${predictedScore !== null ? 'text-primary' : 'text-white'} relative`}>
                                    {predictedScore !== null ? `${(predictedScore * 100).toFixed(1)}%` : '--'}
                                </div>
                            </div>

                            <div className="w-full bg-white/5 p-4 rounded-lg flex items-start gap-3 text-left">
                                <Info className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                                <p className="text-xs text-muted leading-relaxed">
                                    {predictedScore !== null
                                        ? "This habitability consensus score is derived from our Gradient Boosting Ensembles. Further adjustments will recalculate the prediction."
                                        : "Adjust the parameters on the left and run the model to generate a consensus habitability score based on our Gradient Boosting ensembles."
                                    }
                                </p>
                            </div>
                        </Card>
                    </section>

                    {/* Explanation Placeholder */}
                    <section className={`transition-opacity duration-500 ${predictedScore !== null ? 'opacity-100' : 'opacity-50'}`}>
                        <Card className={`p-6 ${predictedScore === null ? 'border-dashed' : ''}`} hoverable={false}>
                            <h4 className="text-sm font-bold mb-4">Feature Influence Explanation (SHAP)</h4>
                            {predictedScore !== null ? (
                                <div className="space-y-3">
                                    <div className="flex justify-between items-center text-xs">
                                        <span className="text-muted">Equilibrium Temperature</span>
                                        <span className="text-success">+0.14</span>
                                    </div>
                                    <div className="w-full bg-white/5 h-1.5 rounded-full"><div className="bg-success h-full rounded-full" style={{ width: '60%' }}></div></div>
                                    <div className="flex justify-between items-center text-xs mt-4">
                                        <span className="text-muted">Planet Radius</span>
                                        <span className="text-danger">-0.05</span>
                                    </div>
                                    <div className="w-full bg-white/5 h-1.5 rounded-full"><div className="bg-danger h-full rounded-full" style={{ width: '30%' }}></div></div>
                                </div>
                            ) : (
                                <div className="h-32 flex items-center justify-center italic text-xs text-muted">
                                    Prediction required to generate feature impact analysis...
                                </div>
                            )}
                        </Card>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default HabitabilitySimulator;

