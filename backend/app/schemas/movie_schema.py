from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class CastMemberCreate(BaseModel):
    name: str
    role: str
    star_power: Optional[float] = None

class MovieCreate(BaseModel):
    title: str
    director: str
    genres: List[str]  # Multiple genres
    budget: Optional[float] = None
    budget_currency: str = "INR"
    release_date: Optional[datetime] = None
    languages: List[str]  # Multiple languages
    region: str
    cast: List[CastMemberCreate] = []
    status: str = "pre-production"

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genres: Optional[List[str]] = None
    budget: Optional[float] = None
    release_date: Optional[datetime] = None
    languages: Optional[List[str]] = None
    region: Optional[str] = None
    cast: Optional[List[CastMemberCreate]] = None
    status: Optional[str] = None

class MovieResponse(BaseModel):
    id: str
    title: str
    director: str
    genres: List[str]
    budget: Optional[float] = None
    budget_currency: str = "INR"
    release_date: Optional[datetime] = None
    languages: List[str] = []
    region: Optional[str] = None
    cast: List[dict] = []
    producer_id: str
    status: str = "pre-production"
    tag: str = "current"  # "past" or "current"
    hws_score: Optional[float] = None
    category: Optional[str] = None  # BIG, MEDIUM, SMALL
    market_action: Optional[str] = None
    hws_breakdown: Optional[dict] = None  # Detailed HWS breakdown
    cast_score: Optional[float] = None
    historic_score: Optional[float] = None
    public_pulse_score: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        extra = 'ignore'  # Ignore extra fields from database

class CompetitorRequest(BaseModel):
    competitor_movie_id: str

class CompetitorAnalysisResponse(BaseModel):
    movie_id: str
    competitor_movie_id: str
    your_movie_title: str
    competitor_movie_title: str
    your_cast_score: float
    competitor_cast_score: float
    your_historic_score: float
    competitor_historic_score: float
    your_pulse_score: float
    competitor_pulse_score: float
    overall_strength: str
    recommendation: str
    release_date_conflict: bool
    days_apart: int
