import { Link, useLocation } from 'react-router-dom';
import { Compass, Activity, Cpu, BookOpen, Home, Zap } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: any[]) {
    return twMerge(clsx(inputs));
}

const Navbar = () => {
    const location = useLocation();

    const navItems = [
        { name: 'Home', path: '/', icon: Home },
        { name: 'Discovery Explorer', path: '/explorer', icon: Compass },
        { name: 'Habitability Simulator', path: '/simulator', icon: Activity },
        { name: 'AI Insights', path: '/insights', icon: Cpu },
        { name: 'Research', path: '/research', icon: BookOpen },
    ];

    return (
        <nav className="sticky top-0 z-50 glass-panel border-b border-white/10 px-6 py-4">
            <div className="max-w-7xl mx-auto flex items-center justify-between">
                <Link to="/" className="flex items-center gap-2 group">
                    <div className="bg-primary/20 p-2 rounded-lg group-hover:bg-primary/30 transition-colors">
                        <Zap className="w-6 h-6 text-primary" />
                    </div>
                    <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-white to-muted bg-clip-text text-transparent">
                        ExoIntel
                    </span>
                </Link>

                <div className="hidden md:flex items-center gap-6">
                    {navItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = location.pathname === item.path;

                        return (
                            <Link
                                key={item.path}
                                to={item.path}
                                className={cn(
                                    "flex items-center gap-2 text-sm font-medium transition-all duration-200 hover:text-white",
                                    isActive ? "text-primary" : "text-muted"
                                )}
                            >
                                <Icon className="w-4 h-4" />
                                {item.name}
                            </Link>
                        );
                    })}
                </div>

                <div className="flex items-center gap-4">
                    <button className="bg-primary hover:bg-primary/80 text-white px-4 py-2 rounded-lg text-sm font-semibold transition-all shadow-lg shadow-primary/20">
                        Login
                    </button>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
