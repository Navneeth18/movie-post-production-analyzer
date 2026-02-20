from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ReleaseDateAnalysisRequest(BaseModel):
    movie_id: str
    target_release_date: Optional[datetime] = None
    days_before: Optional[int] = 30
    days_after: Optional[int] = 30

class CompetitorInDateRange(BaseModel):
    movie_id: str
    title: str
    director: str
    genre: str
    budget: float
    release_date: datetime
    category: str  # "big", "medium", "small"
    cast_score: float
    historic_score: float
    public_pulse_score: float
    days_from_your_release: int
    threat_level: str  # "high", "medium", "low"
    language: str
    region: str

class ReleaseDateAnalysisResponse(BaseModel):
    movie_id: str
    your_movie_title: str
    your_movie_category: str
    target_release_date: datetime
    date_range_start: datetime
    date_range_end: datetime
    total_competitors: int
    competitors: List[CompetitorInDateRange]
    big_movies_count: int
    medium_movies_count: int
    small_movies_count: int
    high_threat_count: int
    recommendation: str
    optimal_release_windows: List[dict]
    risk_assessment: str

class PRStrategyRequest(BaseModel):
    movie_id: str
    competitor_movie_ids: Optional[List[str]] = []
    focus_areas: Optional[List[str]] = ["social_media", "press", "influencer", "events"]

class PRStrategyResponse(BaseModel):
    movie_id: str
    movie_title: str
    movie_category: str
    pr_strategy: str
    key_differentiators: List[str]
    target_audience_approach: dict
    media_channels: List[dict]
    timeline: List[dict]
    budget_allocation: dict
    risk_mitigation: List[str]
    success_metrics: List[str]
