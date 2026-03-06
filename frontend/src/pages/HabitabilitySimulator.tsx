import { Sliders, Play, Info } from 'lucide-react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';

const HabitabilitySimulator = () => {
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
                            <button className="text-xs text-primary hover:underline">Reset to Earth-Standard</button>
                        </div>

                        <div className="grid gap-6">
                            {[
                                { label: 'Planet Radius (Earth Radii)', min: 0.1, max: 2.5, val: 1.0 },
                                { label: 'Planet Mass (Earth Masses)', min: 0.1, max: 10.0, val: 1.0 },
                                { label: 'Effective Temperature (K)', min: 50, max: 2000, val: 288 },
                                { label: 'Orbital Semimajor Axis (AU)', min: 0.01, max: 50.0, val: 1.0 },
                                { label: 'Stellar Luminosity (Solar)', min: 0.001, max: 100.0, val: 1.0 },
                            ].map((param, idx) => (
                                <div key={idx} className="space-y-3">
                                    <div className="flex justify-between text-xs font-medium">
                                        <span className="text-muted">{param.label}</span>
                                        <span className="text-primary font-mono">{param.val}</span>
                                    </div>
                                    <div className="h-1.5 w-full bg-white/5 rounded-full relative">
                                        <div className="absolute top-0 left-0 h-full bg-primary rounded-full" style={{ width: '40%' }} />
                                    </div>
                                </div>
                            ))}
                        </div>

                        <Button className="w-full gap-2" size="lg">
                            <Play className="w-4 h-4 fill-current" />
                            Run Prediction Model
                        </Button>
                    </Card>
                </section>

                {/* Prediction Output Section */}
                <div className="space-y-8">
                    <section className="h-full">
                        <Card className="p-8 flex flex-col items-center justify-center text-center h-full">
                            <div className="space-y-2 mb-8">
                                <h3 className="text-sm font-bold uppercase tracking-widest text-muted">Habitability Index</h3>
                                <div className="text-6xl font-bold text-white relative">
                                    --
                                </div>
                            </div>

                            <div className="w-full bg-white/5 p-4 rounded-lg flex items-start gap-3 text-left">
                                <Info className="w-5 h-5 text-primary shrink-0 mt-0.5" />
                                <p className="text-xs text-muted leading-relaxed">
                                    Adjust the parameters on the left and run the model to generate a consensus habitability score based on our Gradient Boosting ensembles.
                                </p>
                            </div>
                        </Card>
                    </section>

                    {/* Explanation Placeholder */}
                    <section className="opacity-50">
                        <Card className="p-6 border-dashed" hoverable={false}>
                            <h4 className="text-sm font-bold mb-4">Feature Influence Explanation (SHAP)</h4>
                            <div className="h-32 flex items-center justify-center italic text-xs text-muted">
                                Prediction required to generate feature impact analysis...
                            </div>
                        </Card>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default HabitabilitySimulator;
