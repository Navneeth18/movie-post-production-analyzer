"""
Facebook Campaign Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class FacebookPostRequest(BaseModel):
    movie_name: str
    hero_name: str
    heroine_name: str
    director_name: str
    genre: str
    release_date: Optional[str] = None  # YYYY-MM-DD format
    requirements_poster: Optional[str] = None  # Custom poster requirements

class CampaignContentRequest(BaseModel):
    campaign_type: str  # teaser, trailer, countdown, release, cast_reveal

class CampaignScheduleRequest(BaseModel):
    campaign_duration_days: int = 30  # Days before release to start campaign

class FacebookPostResponse(BaseModel):
    success: bool
    post_id: Optional[str] = None
    scheduled: bool = False
    scheduled_time: Optional[datetime] = None
    image_url: Optional[str] = None  # URL of generated or provided image
    mock: bool = False
    error: Optional[str] = None
    message: Optional[str] = None

class CampaignContentResponse(BaseModel):
    message: str
    hashtags: List[str]
    suggestion: str
    image_prompt: str  # AI prompt for image generation
    campaign_type: str

class ScheduledPostResponse(BaseModel):
    title: str
    scheduled_date: datetime
    campaign_type: str
    message: str
    hashtags: List[str]
    suggestion: str
    status: str  # pending, posted, failed

class PostInsightsResponse(BaseModel):
    success: bool
    impressions: int = 0
    engaged_users: int = 0
    clicks: int = 0
    mock: bool = False
