import { Search, Filter, ChevronRight, Globe } from 'lucide-react';

const DiscoveryExplorer = () => {
    return (
        <div className="space-y-8">
            <header className="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h1 className="text-3xl font-bold">Discovery Explorer</h1>
                    <p className="text-muted">Analyze and browse candidate planets identified by our AI.</p>
                </div>

                <div className="flex gap-4">
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted group-focus-within:text-primary transition-colors" />
                        <input
                            type="text"
                            placeholder="Search by planet name..."
                            className="bg-surface border border-white/5 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-primary/50 transition-all w-64"
                        />
                    </div>
                    <button className="flex items-center gap-2 bg-surface hover:bg-white/5 border border-white/5 px-4 py-2 rounded-lg text-sm transition-all">
                        <Filter className="w-4 h-4" />
                        Filter
                    </button>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Table Section */}
                <section className="lg:col-span-2 cosmic-card">
                    <div className="overflow-x-auto">
                        <table className="w-full text-left text-sm">
                            <thead className="bg-[#0c0c25] border-b border-white/5 text-muted font-medium uppercase tracking-wider text-xs">
                                <tr>
                                    <th className="px-6 py-4">Planet Name</th>
                                    <th className="px-6 py-4">Score</th>
                                    <th className="px-6 py-4">Distance (pc)</th>
                                    <th className="px-6 py-4">Status</th>
                                    <th className="px-6 py-4"></th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-white/5">
                                {[
                                    { name: 'K2-18 b', score: 0.89, dist: 38, status: 'Confirmed' },
                                    { name: 'Gliese 12 b', score: 0.94, dist: 12, status: 'Candidate' },
                                    { name: 'Proxima Cen b', score: 0.91, dist: 1.3, status: 'Confirmed' },
                                    { name: 'TRAPPIST-1 e', score: 0.88, dist: 12.1, status: 'Confirmed' },
                                    { name: 'Kepler-186 f', score: 0.82, dist: 178, status: 'Confirmed' },
                                ].map((item, idx) => (
                                    <tr key={idx} className="hover:bg-white/[0.02] cursor-pointer group transition-colors">
                                        <td className="px-6 py-4 font-medium flex items-center gap-3">
                                            <div className="w-2 h-2 rounded-full bg-success shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                                            {item.name}
                                        </td>
                                        <td className="px-6 py-4">
                                            <span className="font-mono text-primary">{(item.score * 100).toFixed(1)}%</span>
                                        </td>
                                        <td className="px-6 py-4 text-muted">{item.dist}</td>
                                        <td className="px-6 py-4">
                                            <span className="bg-primary/10 text-primary px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight">
                                                {item.status}
                                            </span>
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <ChevronRight className="w-4 h-4 text-muted group-hover:text-white transition-colors ml-auto" />
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* Detail Sidebar Selection Placeholder */}
                <aside className="cosmic-card p-6 flex flex-col items-center justify-center text-center space-y-4">
                    <div className="bg-surface p-6 rounded-full border border-white/5">
                        <Globe className="w-12 h-12 text-primary animate-pulse" />
                    </div>
                    <div className="space-y-1">
                        <h3 className="font-bold">Select a Candidate</h3>
                        <p className="text-sm text-muted">Click on a planet in the discovery list to view detailed habitability analysis and SHAP explanations.</p>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default DiscoveryExplorer;
