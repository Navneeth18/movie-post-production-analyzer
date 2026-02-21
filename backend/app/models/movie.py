from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class HistoricalMovieModel(BaseModel):
    """Database representation of past movies from Bhanu dataset."""
    movie_name: str
    hero: Optional[str]
    heroine: Optional[str]
    director: Optional[str]
    budget: int = 0
    revenue: int = 0
    imdb_rating: Optional[float] = 0.0
    popularity_score: float = 0.0
    genre: Optional[str]
    release_date: Optional[str]
    tag: str = "past"  # "past" for historical movies

class ActiveProjectModel(BaseModel):
    """Representation of the current movie a producer is analyzing."""
    producer_id: str
    movie_name: str
    hws_score: float
    category: str  # Big, Medium, Small
    created_at: datetime = Field(default_factory=datetime.utcnow)
    youtube_video_id: Optional[str] = None
    sentiment_history: List[dict] = []  # Stores snapshots of pulse scores
    tag: str = "current"  # "current" for active projects

class CastMember(BaseModel):
    name: str
    role: str
    star_power: Optional[float] = None  # 0-100 score

class Movie(BaseModel):
    """New movie model for producer projects"""
    title: str
    director: str
    genres: List[str]  # Multiple genres
    budget: Optional[float] = None
    budget_currency: str = "INR"
    release_date: Optional[datetime] = None
    languages: List[str]  # Multiple languages
    region: str
    cast: List[CastMember] = []
    producer_id: str  # User ID of the producer
    status: str = "pre-production"  # pre-production, production, post-production, awaiting-release, released
    tag: str = "current"  # "past" or "current"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Scores
    hws_score: Optional[float] = None
    cast_score: Optional[float] = None
    historic_score: Optional[float] = None
    public_pulse_score: Optional[float] = None
    
class MovieInDB(Movie):
    id: str
