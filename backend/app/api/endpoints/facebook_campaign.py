"""
Facebook Campaign API Endpoints
Handles automated Facebook posting and campaign management for movie PR
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from datetime import datetime
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.services.facebook_service import FacebookService
from app.schemas.facebook_schema import (
    FacebookPostRequest,
    FacebookPostResponse,
    CampaignContentRequest,
    CampaignContentResponse,
    CampaignScheduleRequest,
    ScheduledPostResponse,
    PostInsightsResponse
)

router = APIRouter()

@router.post("/{movie_id}/create-post", response_model=FacebookPostResponse)
async def create_facebook_post(
    movie_id: str,
    request: FacebookPostRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create Facebook post with AI-generated poster
    Follows the exact pattern from movie_promo_auto_post.py
    (Only for current/unreleased movies)
    """
    db = get_database()
    
    # Get movie
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a current movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400,
            detail="Facebook campaigns are only available for unreleased movies"
        )
    
    # Prepare movie data exactly like your script
    movie_data = {
        'movie_name': request.movie_name,
        'hero_name': request.hero_name,
        'heroine_name': request.heroine_name,
        'director_name': request.director_name,
        'genre': request.genre,
        'release_date': request.release_date,
        'requirements_poster': request.requirements_poster
    }
    
    # Create post with automatic poster generation
    fb_service = FacebookService()
    result = await fb_service.create_post(movie_data)
    
    # Store post in database
    post_doc = {
        'movie_id': movie_id,
        'producer_id': str(current_user["_id"]),
        'post_id': result.get('post_id'),
        'movie_data': movie_data,
        'caption': result.get('caption'),
        'image_generated': bool(result.get('image_url')),
        'created_at': datetime.utcnow(),
        'status': 'posted',
        'mock': result.get('mock', False)
    }
    await db.facebook_posts.insert_one(post_doc)
    
    return FacebookPostResponse(**result)

@router.get("/{movie_id}/posts", response_model=List[dict])
async def get_movie_posts(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get all Facebook posts for a movie
    """
    db = get_database()
    
    # Get movie
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get posts
    posts = await db.facebook_posts.find({
        'movie_id': movie_id
    }).sort('created_at', -1).to_list(100)
    
    return [
        {
            'id': str(post['_id']),
            'post_id': post.get('post_id'),
            'caption': post.get('caption', ''),
            'created_at': post.get('created_at'),
            'status': post.get('status'),
            'mock': post.get('mock', False)
        }
        for post in posts
    ]

