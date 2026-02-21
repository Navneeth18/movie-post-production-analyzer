"""
Public Pulse API Endpoints
Handles YouTube trailer analysis and sentiment tracking over time
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from datetime import datetime
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.services.youtube_sentiment_service import YouTubeSentimentService
from pydantic import BaseModel

router = APIRouter()

class YouTubeTrailerRequest(BaseModel):
    youtube_url: str

class PublicPulseResponse(BaseModel):
    movie_id: str
    movie_title: str
    youtube_video_id: str
    current_pulse_score: float
    likes: int
    dislikes: int
    views: int
    engagement_rate: float
    sentiment: str
    last_updated: datetime

class PulseHistoryResponse(BaseModel):
    date: datetime
    pulse_score: float
    likes: int
    dislikes: int
    views: int
    comments_analyzed: int

@router.post("/{movie_id}/add-trailer")
async def add_youtube_trailer(
    movie_id: str,
    trailer_data: YouTubeTrailerRequest,
    current_user: dict = Depends(get_current_user)
):
    """Add YouTube trailer link to movie and calculate initial pulse (current movies only)"""
    db = get_database()
    
    # Verify movie ownership and that it's a current movie
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a current movie (not historical)
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400, 
            detail="Public pulse is only available for current movies, not historical movies"
        )
    
    # Extract video ID from URL
    video_id = YouTubeSentimentService.extract_video_id(trailer_data.youtube_url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")
    
    # Fetch YouTube data
    try:
        yt_data = await YouTubeSentimentService.fetch_youtube_data(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch YouTube data: {str(e)}")
    
    # Calculate public pulse
    pulse_score = YouTubeSentimentService.calculate_public_pulse(
        title=movie["title"],
        youtube_video_id=video_id,
        likes=yt_data.get('likes', 0),
        dislikes=yt_data.get('dislikes', 0),
        views=yt_data.get('views', 0),
        comments=yt_data.get('comments', [])
    )
    
    # Update movie with YouTube data
    await db.movies.update_one(
        {"_id": ObjectId(movie_id)},
        {
            "$set": {
                "youtube_video_id": video_id,
                "youtube_url": trailer_data.youtube_url,
                "public_pulse_score": pulse_score,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Store initial pulse history
    pulse_history = {
        "movie_id": movie_id,
        "pulse_score": pulse_score,
        "likes": yt_data.get('likes', 0),
        "dislikes": yt_data.get('dislikes', 0),
        "views": yt_data.get('views', 0),
        "comments_analyzed": len(yt_data.get('comments', [])),
        "recorded_at": datetime.utcnow()
    }
    await db.pulse_history.insert_one(pulse_history)
    
    return {
        "message": "Trailer added successfully",
        "video_id": video_id,
        "pulse_score": pulse_score,
        "youtube_data": yt_data
    }

@router.post("/{movie_id}/refresh-pulse")
async def refresh_public_pulse(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Refresh public pulse data from YouTube (current movies only)"""
    db = get_database()
    
    # Verify movie ownership
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a current movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400, 
            detail="Public pulse is only available for current movies"
        )
    
    video_id = movie.get("youtube_video_id")
    if not video_id:
        raise HTTPException(status_code=400, detail="No YouTube trailer linked to this movie")
    
    # Fetch latest YouTube data
    try:
        yt_data = await YouTubeSentimentService.fetch_youtube_data(video_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch YouTube data: {str(e)}")
    
    # Calculate new pulse score
    pulse_score = YouTubeSentimentService.calculate_public_pulse(
        title=movie["title"],
        youtube_video_id=video_id,
        likes=yt_data.get('likes', 0),
        dislikes=yt_data.get('dislikes', 0),
        views=yt_data.get('views', 0),
        comments=yt_data.get('comments', [])
    )
    
    # Update movie
    await db.movies.update_one(
        {"_id": ObjectId(movie_id)},
        {
            "$set": {
                "public_pulse_score": pulse_score,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Store in history
    pulse_history = {
        "movie_id": movie_id,
        "pulse_score": pulse_score,
        "likes": yt_data.get('likes', 0),
        "dislikes": yt_data.get('dislikes', 0),
        "views": yt_data.get('views', 0),
        "comments_analyzed": len(yt_data.get('comments', [])),
        "recorded_at": datetime.utcnow()
    }
    await db.pulse_history.insert_one(pulse_history)
    
    return {
        "message": "Public pulse refreshed",
        "pulse_score": pulse_score,
        "youtube_data": yt_data
    }

@router.get("/{movie_id}/current", response_model=PublicPulseResponse)
async def get_current_pulse(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get current public pulse data for a movie (current movies only)"""
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a current movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400, 
            detail="Public pulse is only available for current movies"
        )
    
    if not movie.get("youtube_video_id"):
        raise HTTPException(status_code=404, detail="No YouTube trailer linked")
    
    # Get latest pulse history
    latest_pulse = await db.pulse_history.find_one(
        {"movie_id": movie_id},
        sort=[("recorded_at", -1)]
    )
    
    if not latest_pulse:
        raise HTTPException(status_code=404, detail="No pulse data available")
    
    pulse_score = movie.get("public_pulse_score", 0)
    likes = latest_pulse.get("likes", 0)
    dislikes = latest_pulse.get("dislikes", 0)
    views = latest_pulse.get("views", 0)
    
    # Calculate engagement rate
    engagement_rate = ((likes + dislikes) / views * 100) if views > 0 else 0
    
    # Determine sentiment
    if pulse_score >= 70:
        sentiment = "Positive"
    elif pulse_score >= 50:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    
    return PublicPulseResponse(
        movie_id=movie_id,
        movie_title=movie["title"],
        youtube_video_id=movie["youtube_video_id"],
        current_pulse_score=pulse_score,
        likes=likes,
        dislikes=dislikes,
        views=views,
        engagement_rate=round(engagement_rate, 2),
        sentiment=sentiment,
        last_updated=latest_pulse["recorded_at"]
    )

@router.get("/{movie_id}/history", response_model=List[PulseHistoryResponse])
async def get_pulse_history(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get historical public pulse data for graphing"""
    db = get_database()
    
    # Verify movie ownership
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get pulse history sorted by date
    history = await db.pulse_history.find(
        {"movie_id": movie_id}
    ).sort("recorded_at", 1).to_list(100)
    
    return [
        PulseHistoryResponse(
            date=h["recorded_at"],
            pulse_score=h["pulse_score"],
            likes=h.get("likes", 0),
            dislikes=h.get("dislikes", 0),
            views=h.get("views", 0),
            comments_analyzed=h.get("comments_analyzed", 0)
        )
        for h in history
    ]

@router.delete("/{movie_id}/trailer")
async def remove_trailer(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Remove YouTube trailer link from movie"""
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Remove YouTube data from movie
    await db.movies.update_one(
        {"_id": ObjectId(movie_id)},
        {
            "$unset": {
                "youtube_video_id": "",
                "youtube_url": "",
                "public_pulse_score": ""
            },
            "$set": {
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    # Optionally delete pulse history
    # await db.pulse_history.delete_many({"movie_id": movie_id})
    
    return {"message": "Trailer removed successfully"}
