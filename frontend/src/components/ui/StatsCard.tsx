import React from 'react';
import { LucideIcon } from 'lucide-react';
import Card from './Card';

interface StatsCardProps {
    label: string;
    value: string | number;
    icon: LucideIcon;
    color?: string;
    description?: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ label, value, icon: Icon, color = 'text-primary', description }) => {
    return (
        <Card className="p-6 space-y-4">
            <div className="flex items-center justify-between">
                <div className={`p-2 rounded-lg bg-surface border border-white/5`}>
                    <Icon className={`w-6 h-6 ${color}`} />
                </div>
            </div>
            <div>
                <p className="text-xs font-medium text-muted uppercase tracking-wider">{label}</p>
                <h3 className="text-2xl font-bold mt-1">{value}</h3>
                {description && <p className="text-xs text-muted mt-2">{description}</p>}
            </div>
        </Card>
    );
};

export default StatsCard;
