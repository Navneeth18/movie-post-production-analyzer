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
    genre: str
    budget: Optional[float] = None
    budget_currency: str = "INR"
    release_date: Optional[datetime] = None
    language: str
    themes: Optional[str] = None
    region: str
    cast: List[CastMemberCreate] = []
    status: str = "pre-production"

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    budget: Optional[float] = None
    release_date: Optional[datetime] = None
    language: Optional[str] = None
    themes: Optional[str] = None
    region: Optional[str] = None
    cast: Optional[List[CastMemberCreate]] = None
    status: Optional[str] = None

class MovieResponse(BaseModel):
    id: str
    title: str
    director: str
    genre: str
    budget: Optional[float]
    budget_currency: str
    release_date: Optional[datetime]
    language: str
    themes: Optional[str]
    region: str
    cast: List[dict]
    producer_id: str
    status: str
    tag: str  # "past" or "current"
    hws_score: Optional[float]
    cast_score: Optional[float]
    historic_score: Optional[float]
    public_pulse_score: Optional[float]
    created_at: datetime
    updated_at: datetime

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
