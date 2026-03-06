import React from 'react';

interface PageContainerProps {
    children: React.ReactNode;
}

const PageContainer: React.FC<PageContainerProps> = ({ children }) => {
    return (
        <main className="flex-grow w-full max-w-7xl mx-auto px-6 py-12">
            {children}
        </main>
    );
};

export default PageContainer;
