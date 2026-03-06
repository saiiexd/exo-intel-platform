import React from 'react';
import { Rocket, Shield, Target, Zap } from 'lucide-react';
import Button from '@/components/ui/Button';
import StatsCard from '@/components/ui/StatsCard';
import Card from '@/components/ui/Card';

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
                    <Button size="lg">Launch Explorer</Button>
                    <Button size="lg" variant="outline">View Methodology</Button>
                </div>
            </section>

            {/* Stats Section */}
            <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {homeStats.map((stat, idx) => (
                    <StatsCard
                        key={idx}
                        label={stat.label}
                        value={stat.value}
                        icon={stat.icon}
                        color={stat.color}
                    />
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
                <Card className="aspect-video border-dashed border-2 flex items-center justify-center text-muted italic" hoverable={false}>
                    [Interactive 3D Visualizer Placeholder]
                </Card>
            </section>
        </div>
    );
};

export default Home;
