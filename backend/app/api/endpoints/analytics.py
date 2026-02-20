from fastapi import APIRouter

router = APIRouter()

@router.get("/sentiment")
def get_sentiment():
    """Get sentiment analysis for a movie"""
    return {"message": "Sentiment analysis endpoint", "sentiment_score": 65.0}

@router.get("/pulse")
def get_pulse():
    """Get public pulse score for a movie"""
    return {"message": "Pulse analysis endpoint", "pulse_score": 70.0}
