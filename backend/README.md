# Film Intel Backend

Backend API for the Film Intelligence Platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`

3. Run with Docker:
```bash
docker-compose up
```

4. Or run locally:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `/api/v1/analytics/sentiment` - Sentiment analysis
- `/api/v1/analytics/pulse` - Pulse analysis
- `/api/v1/calculator/hws` - HWS score calculation
- `/api/v1/marketing/meme` - Meme generation
- `/api/v1/marketing/twitter` - Twitter automation
- `/api/v1/strategy/reasoning` - AI reasoning (DeepSeek)
