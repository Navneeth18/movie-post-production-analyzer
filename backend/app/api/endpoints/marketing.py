from fastapi import APIRouter
from app.services.ai_service import AIService
from app.core.config import settings
from pydantic import BaseModel

router = APIRouter()
ai_service = AIService(settings.OLLAMA_URL)

class MemeRequest(BaseModel):
    genre: str
    theme: str

@router.post("/generate-meme")
async def create_meme(data: MemeRequest):
    # Get a caption/idea from DeepSeek first
    idea_prompt = f"Write a 1-sentence sarcastic meme caption for a {data.genre} movie about {data.theme}."
    caption = ai_service.generate_strategy({"genre": data.genre, "hero": "the protagonist", "score": "N/A"}) # Reusing strategy logic for caption
    
    # Generate image URL via Pollinations
    image_url = ai_service.generate_meme_url(data.genre, data.theme)
    
    return {
        "image_url": image_url,
        "caption": caption.split("\n")[-1], # Get the last line of reasoning
        "platform": "YouTube/Community"
    }