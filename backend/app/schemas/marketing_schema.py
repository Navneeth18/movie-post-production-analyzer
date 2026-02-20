from pydantic import BaseModel, HttpUrl
from typing import Optional

class MemeCreate(BaseModel):
    genre: str
    theme: str
    target_audience: Optional[str] = "General"

class MemeResponse(BaseModel):
    image_url: str
    suggested_caption: str
    reasoning: Optional[str] # DeepSeek's logic for the meme

class PulseResponse(BaseModel):
    sentiment_score: float
    hype_status: str
    top_keywords: List[str]