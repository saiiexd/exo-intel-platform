# ExoIntel Frontend – Interactive Discovery Interface

This is the professional interactive discovery interface for the ExoIntel AI Exoplanet Discovery Platform. It provides a modern, scientific UI for researchers and explorers to interact with the platform's discovery engines and ML models.

## Technology Stack
- **Framework**: React 18 (TypeScript)
- **Styling**: TailwindCSS
- **Routing**: React Router 6
- **Icons**: Lucide React
- **Data Viz**: Recharts (Placeholder structured)
- **API Client**: Axios

## Getting Started

### Prerequisites
- Node.js 18+
- npm

### Installation
```bash
cd frontend
npm install
```

### Development
Launch the development server:
```bash
npm run dev
```

### Production Build
Create an optimized production bundle:
```bash
npm run build
```

## Architecture
- `src/components`: Reusable UI components and layout fragments.
- `src/pages`: Top-level page components and route targets.
- `src/services`: API client and backend service wrappers.
- `src/types`: Centralized TypeScript interface definitions.
- `src/styles`: Tailwind global styles and design tokens.
