/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: "#050510",
                surface: "#0a0a1f",
                primary: "#3b82f6", // Cosmic Blue
                secondary: "#8b5cf6", // Purple
                accent: "#06b6d4", // Cyan
                muted: "#94a3b8",
                success: "#10b981",
                warning: "#f59e0b",
                error: "#ef4444",
            },
            backgroundImage: {
                'cosmic-gradient': 'linear-gradient(to bottom right, #050510, #0a0a2e, #1e1e4a)',
            }
        },
    },
    plugins: [],
}
