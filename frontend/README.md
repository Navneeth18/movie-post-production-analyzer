# Film Intel Frontend

React-based frontend for the Film Intelligence Platform.

## Features

- Dashboard with HWS score calculation
- Audience DNA profiling
- Campaign ROI simulator
- Distribution platform matching
- Festival submission strategy
- AI-powered insights and recommendations

## Tech Stack

- React 19
- Vite
- React Router
- Axios for API calls
- Zustand for state management
- Recharts for data visualization

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables in `.env`:
```
VITE_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

4. Build for production:
```bash
npm run build
```

## Project Structure

```
src/
├── components/     # Reusable UI components
├── pages/          # Page components
├── services/       # API service layer
├── hooks/          # Custom React hooks
├── store/          # Zustand state management
├── utils/          # Utility functions and constants
├── config/         # Configuration files
└── styles/         # Global styles
```

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/api/v1`. All API calls are centralized in `src/services/api.js`.

### Available Endpoints

- `/analytics/sentiment` - Sentiment analysis
- `/analytics/pulse` - Pulse analysis
- `/calculator/hws` - HWS score calculation
- `/marketing/meme` - Meme generation
- `/marketing/twitter` - Twitter automation
- `/strategy/reasoning` - AI reasoning

## Development

Run the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`
