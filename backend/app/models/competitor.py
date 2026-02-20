from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Competitor(BaseModel):
    movie_id: str  # The user's movie
    competitor_movie_id: str  # Competing movie
    release_date_proximity: int  # Days difference
    genre_overlap: float  # 0-1 similarity score
    target_audience_overlap: float  # 0-1 similarity score
    strength_comparison: Optional[str] = None  # "stronger", "weaker", "equal"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class CompetitorInDB(Competitor):
    id: str

class CompetitorAnalysis(BaseModel):
    movie_id: str
    competitor_movie_id: str
    your_movie_title: str
    competitor_movie_title: str
    
    # Comparative scores
    your_cast_score: float
    competitor_cast_score: float
    your_historic_score: float
    competitor_historic_score: float
    your_pulse_score: float
    competitor_pulse_score: float
    
    # Overall comparison
    overall_strength: str  # "stronger", "weaker", "equal"
    recommendation: str
    release_date_conflict: bool
    days_apart: int
