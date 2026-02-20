from fastapi import APIRouter
from app.services.ai_service import AIService
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()
ai_service = AIService(settings.OLLAMA_URL)

class StrategyRequest(BaseModel):
    movie_name: str
    genre: str
    hero: str
    hws_score: float

@router.post("/get-reasoning")
async def get_market_strategy(data: StrategyRequest):
    details = {
        "genre": data.genre,
        "hero": data.hero,
        "score": data.hws_score
    }
    advice = ai_service.generate_strategy(details)
    return {
        "movie": data.movie_name,
        "marketing_plan": advice,
        "suggested_action": "Theatrical" if data.hws_score > 60 else "OTT Pivot"
    }