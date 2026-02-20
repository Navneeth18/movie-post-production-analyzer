# Film Intel Platform

Full-stack Film Intelligence Platform for producers to analyze, strategize, and optimize their film projects.

## Architecture

- **Frontend**: React + Vite (Port 5173)
- **Backend**: FastAPI + Python (Port 8000)
- **Database**: MongoDB
- **AI**: Ollama (local) + DeepSeek API
- **Vector DB**: ChromaDB for sentiment analysis

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at `http://localhost:5173`

### Docker Setup (Optional)

```bash
cd backend
docker-compose up
```

## Features

- HWS Score Calculator (Hollywood-Weighted Score)
- Audience DNA Profiling
- Campaign ROI Simulator
- Distribution Platform Matching
- Festival Submission Strategy
- AI Strategy Advisor
- Film Comparables Analysis

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=film_intel
OLLAMA_BASE_URL=http://localhost:11434
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
DEEPSEEK_API_KEY=your_key
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Film Intel Platform
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

```
film_intel_backend/
├── app/
│   ├── api/endpoints/    # API routes
│   ├── core/             # Configuration
│   ├── db/               # Database connections
│   ├── models/           # Data models
│   ├── schemas/          # Request/response schemas
│   └── services/         # Business logic
├── data/                 # CSV datasets
└── scripts/              # Utility scripts

frontend/
├── src/
│   ├── components/       # UI components
│   ├── pages/            # Page components
│   ├── services/         # API layer
│   ├── hooks/            # Custom hooks
│   ├── store/            # State management
│   └── utils/            # Utilities
```

## License

Proprietary
