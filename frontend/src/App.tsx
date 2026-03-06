import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from '@/components/layout/Navbar';
import Footer from '@/components/layout/Footer';
import PageContainer from '@/components/layout/PageContainer';

// Lazy loading pages for better structure
import Home from '@/pages/Home';
import DiscoveryExplorer from '@/pages/DiscoveryExplorer';
import HabitabilitySimulator from '@/pages/HabitabilitySimulator';
import AIInsights from '@/pages/AIInsights';
import Research from '@/pages/Research';

function App() {
    return (
        <Router>
            <div className="flex flex-col min-h-screen bg-background bg-cosmic-gradient">
                <Navbar />
                <PageContainer>
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/explorer" element={<DiscoveryExplorer />} />
                        <Route path="/simulator" element={<HabitabilitySimulator />} />
                        <Route path="/insights" element={<AIInsights />} />
                        <Route path="/research" element={<Research />} />
                    </Routes>
                </PageContainer>
                <Footer />
            </div>
        </Router>
    );
}

export default App;
