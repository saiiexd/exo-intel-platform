import { useState } from 'react';
import { Search, Filter, ChevronRight, Globe, Info } from 'lucide-react';
import Card from '@/components/ui/Card';
import Button from '@/components/ui/Button';
import { useExoplanets } from '../hooks/useExoplanets';

const DiscoveryExplorer = () => {
    const { planets, loading } = useExoplanets();
    const [selectedPlanetName, setSelectedPlanetName] = useState<string | null>(null);

    const selectedPlanet = planets.find(p => (p.name || (p as any).planet_name) === selectedPlanetName);

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
                    <Button variant="outline" className="gap-2">
                        <Filter className="w-4 h-4" />
                        Filter
                    </Button>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Table Section */}
                <section className="lg:col-span-2">
                    <Card className="p-0">
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
                                    {loading ? (
                                        <tr>
                                            <td colSpan={5} className="text-center py-8 text-muted">Loading candidates...</td>
                                        </tr>
                                    ) : planets.map((item: any, idx) => {
                                        const name = item.name || item.planet_name || 'Unknown';
                                        const score = item.score ?? item.combined_discovery_score ?? 0;
                                        const dist = item.dist ?? item.distance_pc ?? 'N/A';
                                        const status = item.status ?? 'Target';

                                        return (
                                            <tr
                                                key={idx}
                                                onClick={() => setSelectedPlanetName(name)}
                                                className="hover:bg-white/[0.02] cursor-pointer group transition-colors"
                                            >
                                                <td className="px-6 py-4 font-medium flex items-center gap-3">
                                                    <div className="w-2 h-2 rounded-full bg-success shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                                                    {name}
                                                </td>
                                                <td className="px-6 py-4">
                                                    <span className="font-mono text-primary">{(score * 100).toFixed(1)}%</span>
                                                </td>
                                                <td className="px-6 py-4 text-muted">{dist}</td>
                                                <td className="px-6 py-4">
                                                    <span className="bg-primary/10 text-primary px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-tight">
                                                        {status}
                                                    </span>
                                                </td>
                                                <td className="px-6 py-4 text-right">
                                                    <ChevronRight className="w-4 h-4 text-muted group-hover:text-white transition-colors ml-auto" />
                                                </td>
                                            </tr>
                                        )
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </Card>
                </section>

                {/* Detail Sidebar Selection */}
                <aside>
                    {!selectedPlanet ? (
                        <Card className="p-6 flex flex-col items-center justify-center text-center space-y-4 h-full">
                            <div className="bg-surface p-6 rounded-full border border-white/5">
                                <Globe className="w-12 h-12 text-primary animate-pulse" />
                            </div>
                            <div className="space-y-1">
                                <h3 className="font-bold">Select a Candidate</h3>
                                <p className="text-sm text-muted">Click on a planet in the discovery list to view detailed habitability analysis and SHAP explanations.</p>
                            </div>
                        </Card>
                    ) : (
                        <Card className="p-6 space-y-6 h-full flex flex-col">
                            <div className="space-y-2 border-b border-white/10 pb-4">
                                <div className="flex items-center gap-2">
                                    <Globe className="w-5 h-5 text-primary" />
                                    <h3 className="font-bold text-xl">{selectedPlanetName}</h3>
                                </div>
                                <div className="flex gap-2 text-xs">
                                    <span className="px-2 py-1 rounded bg-success/20 text-success uppercase font-bold tracking-wider">
                                        Habitability: {(((selectedPlanet as any).score ?? (selectedPlanet as any).combined_discovery_score ?? 0) * 100).toFixed(1)}%
                                    </span>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-4 flex-grow">
                                <div className="space-y-1">
                                    <p className="text-xs text-muted uppercase">Distance</p>
                                    <p className="font-mono text-sm">{(selectedPlanet as any).dist ?? (selectedPlanet as any).distance_pc ?? 'N/A'} pc</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-xs text-muted uppercase">Radius (Earth)</p>
                                    <p className="font-mono text-sm">{(selectedPlanet as any).planet_radius_earth ?? 'Unknown'}</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-xs text-muted uppercase">Eq. Temp</p>
                                    <p className="font-mono text-sm">{(selectedPlanet as any).equilibrium_temp_k ?? 'Unknown'} K</p>
                                </div>
                                <div className="space-y-1">
                                    <p className="text-xs text-muted uppercase">Stellar Type</p>
                                    <p className="font-mono text-sm">{(selectedPlanet as any).stellar_type ?? 'Unknown'}</p>
                                </div>
                            </div>

                            <div className="mt-auto pt-4 border-t border-white/10 text-xs text-muted flex gap-2">
                                <Info className="w-4 h-4 shrink-0" />
                                <p>Further SHAP feature importance analysis is available in the AI Insights view or by querying the API directly.</p>
                            </div>
                        </Card>
                    )}
                </aside>
            </div>
        </div>
    );
};

export default DiscoveryExplorer;

