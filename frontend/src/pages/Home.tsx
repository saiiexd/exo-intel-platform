import React from 'react';
import { Rocket, Shield, Target, Zap } from 'lucide-react';

const homeStats = [
    { label: 'Confirmed Planets', value: '5,600+', icon: Target, color: 'text-primary' },
    { label: 'Habitable Candidates', value: '42', icon: Zap, color: 'text-secondary' },
    { label: 'Discovery Accuracy', value: '98.4%', icon: Shield, color: 'text-success' },
];

const Home = () => {
    return (
        <div className="space-y-20">
            {/* Hero Section */}
            <section className="text-center py-20 space-y-8">
                <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 border border-primary/20 text-primary text-xs font-semibold tracking-wider uppercase">
                    <Rocket className="w-3 h-3" />
                    Autonomous Discovery Platform
                </div>
                <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
                    Exploring the Next <br />
                    <span className="text-primary italic">Frontier of Life</span>
                </h1>
                <p className="max-w-2xl mx-auto text-lg text-muted">
                    ExoIntel utilizes advanced machine learning and astrophysical analytics to identify and rank potentially habitable planets across the cosmos.
                </p>
                <div className="flex justify-center gap-4">
                    <button className="bg-primary hover:bg-primary/80 text-white px-8 py-3 rounded-lg font-bold transition-all">
                        Launch Explorer
                    </button>
                    <button className="glass-panel hover:bg-white/5 border border-white/10 px-8 py-3 rounded-lg font-bold transition-all">
                        View Methodology
                    </button>
                </div>
            </section>

            {/* Stats Section */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {homeStats.map((stat, idx) => (
                    <div key={idx} className="cosmic-card p-8 space-y-4">
                        <stat.icon className={`w-8 h-8 ${stat.color}`} />
                        <div>
                            <p className="text-sm font-medium text-muted">{stat.label}</p>
                            <h3 className="text-3xl font-bold">{stat.value}</h3>
                        </div>
                    </div>
                ))}
            </section>

            {/* Platform Overview */}
            <section className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="space-y-6">
                    <h2 className="text-3xl font-bold">Scientific Excellence in Every Computation</h2>
                    <p className="text-muted leading-relaxed">
                        The ExoIntel platform integrates multi-layered astrophysical datasets with state-of-the-art Gradient Boosting models to predict planetary habitability. Our process is transparent, explainable, and built for researchers.
                    </p>
                    <ul className="space-y-4">
                        {[
                            'Direct NASA Exoplanet Archive Integration',
                            'SHAP-based Explainable AI Predictions',
                            'Automated Discovery Pipelines',
                        ].map((item, idx) => (
                            <li key={idx} className="flex items-center gap-3 text-sm font-medium">
                                <div className="w-1.5 h-1.5 rounded-full bg-primary" />
                                {item}
                            </li>
                        ))}
                    </ul>
                </div>
                <div className="cosmic-card aspect-video border-dashed border-2 flex items-center justify-center text-muted italic">
                    [Interactive 3D Visualizer Placeholder]
                </div>
            </section>
        </div>
    );
};

export default Home;
