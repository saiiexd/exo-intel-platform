const Footer = () => {
    return (
        <footer className="mt-auto py-12 px-6 border-t border-white/5 bg-[#030308]">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-4 gap-8">
                <div className="space-y-4">
                    <div className="flex items-center gap-2">
                        <span className="text-xl font-bold tracking-tight">ExoIntel</span>
                    </div>
                    <p className="text-sm text-muted">
                        The professional AI-driven discovery platform for exoplanetary habitability research.
                    </p>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Platform</h4>
                    <ul className="space-y-2 text-sm text-muted">
                        <li>Discovery Explorer</li>
                        <li>Simulations</li>
                        <li>AI Insights</li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Research</h4>
                    <ul className="space-y-2 text-sm text-muted">
                        <li>Methodology</li>
                        <li>Datasets</li>
                        <li>Documentation</li>
                    </ul>
                </div>

                <div>
                    <h4 className="text-white font-semibold mb-4">Legal</h4>
                    <ul className="space-y-2 text-sm text-muted">
                        <li>MIT License</li>
                        <li>Privacy Policy</li>
                    </ul>
                </div>
            </div>

            <div className="max-w-7xl mx-auto mt-12 pt-8 border-t border-white/5 flex justify-between items-center text-xs text-muted">
                <p>&copy; 2026 ExoIntel Platform. All rights reserved.</p>
                <p>Scientific Computing & Discovery Architecture</p>
            </div>
        </footer>
    );
};

export default Footer;
