import React from 'react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: any[]) {
    return twMerge(clsx(inputs));
}

interface CardProps {
    children: React.ReactNode;
    className?: string;
    hoverable?: boolean;
}

const Card: React.FC<CardProps> = ({ children, className, hoverable = true }) => {
    return (
        <div className={cn(
            'glass-panel rounded-xl overflow-hidden border border-white/10 transition-all duration-300',
            hoverable && 'hover:border-primary/50',
            className
        )}>
            {children}
        </div>
    );
};

export default Card;
