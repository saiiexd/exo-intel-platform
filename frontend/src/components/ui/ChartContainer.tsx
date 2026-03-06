import React from 'react';
import Card from './Card';

interface ChartContainerProps {
    title: string;
    children: React.ReactNode;
    description?: string;
    icon?: React.ReactNode;
}

const ChartContainer: React.FC<ChartContainerProps> = ({ title, children, description, icon }) => {
    return (
        <Card className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <h3 className="font-bold flex items-center gap-2 text-sm">
                    {icon}
                    {title}
                </h3>
            </div>
            <div className="h-64 flex items-center justify-center text-muted italic border border-white/5 rounded-lg bg-[#030308]">
                {children}
            </div>
            {description && <p className="text-xs text-muted">{description}</p>}
        </Card>
    );
};

export default ChartContainer;
