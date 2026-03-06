import { Terminal, Database, ShieldCheck, GitBranch } from 'lucide-react';

const Research = () => {
    return (
        <div className="max-w-4xl mx-auto space-y-12">
            <header className="space-y-4">
                <h1 className="text-4xl font-bold tracking-tight">Project Methodology</h1>
                <p className="text-lg text-muted">
                    Understanding the data engineering and machine learning architecture behind the ExoIntel platform.
                </p>
            </header>

            <div className="space-y-16">
                {/* Architecture Section */}
                <section className="space-y-6">
                    <h2 className="text-2xl font-bold flex items-center gap-3">
                        <Database className="w-6 h-6 text-primary" />
                        System Architecture
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {[
                            { title: 'Data Ingestion', desc: 'Real-time API sync with NASA Exoplanet Archive.', icon: Database },
                            { title: 'Discovery Engine', desc: 'Custom ranking algorithms for planetary prioritization.', icon: Target },
                            { title: 'ML Pipeline', desc: 'Ensemble models trained on astrophysical features.', icon: Terminal },
                            { title: 'Explainable AI', desc: 'SHAP interpretations for model transparency.', icon: ShieldCheck },
                        ].map((item, idx) => (
                            <div key={idx} className="cosmic-card p-6 space-y-3">
                                <item.icon className="w-5 h-5 text-primary" />
                                <h4 className="font-bold text-sm uppercase tracking-wide">{item.title}</h4>
                                <p className="text-xs text-muted leading-relaxed">{item.desc}</p>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Workflow Section */}
                <section className="space-y-6">
                    <h2 className="text-2xl font-bold flex items-center gap-3">
                        <GitBranch className="w-6 h-6 text-secondary" />
                        Autonomous Pipeline Workflow
                    </h2>
                    <div className="space-y-4">
                        {[
                            { step: '01', title: 'Data Enrichment', desc: 'Calculation of ESI, Stellar Flux, and Equilibrium Temperature.' },
                            { step: '02', title: 'Model Inference', desc: 'Generating habitability predictions using Gradient Boosting Ensembles.' },
                            { step: '03', title: 'Explainability Generation', desc: 'Computing SHAP values to explain individual planet scores.' },
                            { step: '04', title: 'Insight synthesis', desc: 'Creating professional research reports and data visualizations.' },
                        ].map((item, idx) => (
                            <div key={idx} className="flex gap-6 group">
                                <div className="text-2xl font-mono text-white/10 group-hover:text-primary transition-colors font-bold">
                                    {item.step}
                                </div>
                                <div className="space-y-1">
                                    <h4 className="font-bold">{item.title}</h4>
                                    <p className="text-sm text-muted">{item.desc}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </section>

                {/* Documentation Links */}
                <section className="cosmic-card p-8 bg-primary/5 border-primary/20 space-y-4">
                    <h3 className="font-bold text-lg">Ready to Contribute?</h3>
                    <p className="text-sm text-muted">
                        The ExoIntel platform is open-source under the MIT License. Explore the full technical documentation and source code on GitHub.
                    </p>
                    <div className="flex gap-4 pt-2">
                        <button className="bg-primary text-white px-6 py-2 rounded-lg text-sm font-bold">GitHub Repo</button>
                        <button className="text-primary text-sm font-bold border-b border-primary/30 hover:border-primary transition-all">Technical Docs</button>
                    </div>
                </section>
            </div>
        </div>
    );
};

export default Research;
