from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime, timedelta
from bson import ObjectId
from app.schemas.release_strategy_schema import (
    ReleaseDateAnalysisRequest,
    ReleaseDateAnalysisResponse,
    CompetitorInDateRange,
    PRStrategyRequest,
    PRStrategyResponse
)
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.services.release_strategy_service import ReleaseStrategyService
from app.services.deepseek_service import DeepSeekService

router = APIRouter()

@router.post("/analyze-date-range", response_model=ReleaseDateAnalysisResponse)
async def analyze_release_date_range(
    request: ReleaseDateAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Analyze competitors in a specific date range for a producer's movie.
    Shows big/medium/small movies and their competitive strength.
    """
    db = get_database()
    
    # Get the producer's movie
    movie = await db.movies.find_one({"_id": ObjectId(request.movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Calculate date range (default ±30 days if not provided)
    target_date = request.target_release_date or movie.get("release_date")
    if not target_date:
        raise HTTPException(status_code=400, detail="Release date not set")
    
    days_before = request.days_before or 30
    days_after = request.days_after or 30
    
    start_date = target_date - timedelta(days=days_before)
    end_date = target_date + timedelta(days=days_after)
    
    # Find all movies in date range (excluding user's own movie)
    competitors = await db.movies.find({
        "_id": {"$ne": ObjectId(request.movie_id)},
        "release_date": {
            "$gte": start_date,
            "$lte": end_date
        },
        "status": {"$in": ["awaiting-release", "released"]}
    }).to_list(100)
    
    # Categorize and analyze competitors
    competitor_list = []
    for comp in competitors:
        category = ReleaseStrategyService.categorize_movie(comp)
        days_diff = abs((comp["release_date"] - target_date).days)
        
        # Calculate competitive threat level
        threat_level = ReleaseStrategyService.calculate_threat_level(
            movie, comp, days_diff
        )
        
        competitor_list.append(CompetitorInDateRange(
            movie_id=str(comp["_id"]),
            title=comp["title"],
            director=comp["director"],
            genre=comp["genre"],
            budget=comp.get("budget", 0),
            release_date=comp["release_date"],
            category=category,
            cast_score=comp.get("cast_score", 0),
            historic_score=comp.get("historic_score", 0),
            public_pulse_score=comp.get("public_pulse_score", 0),
            days_from_your_release=days_diff,
            threat_level=threat_level,
            language=comp.get("language", "Unknown"),
            region=comp.get("region", "Unknown")
        ))
    
    # Sort by threat level and date proximity
    competitor_list.sort(key=lambda x: (
        {"high": 0, "medium": 1, "low": 2}[x.threat_level],
        x.days_from_your_release
    ))
    
    # Generate overall analysis
    analysis = ReleaseStrategyService.generate_date_range_analysis(
        movie, competitor_list, target_date
    )
    
    return ReleaseDateAnalysisResponse(
        movie_id=request.movie_id,
        your_movie_title=movie["title"],
        your_movie_category=ReleaseStrategyService.categorize_movie(movie),
        target_release_date=target_date,
        date_range_start=start_date,
        date_range_end=end_date,
        total_competitors=len(competitor_list),
        competitors=competitor_list,
        big_movies_count=len([c for c in competitor_list if c.category == "big"]),
        medium_movies_count=len([c for c in competitor_list if c.category == "medium"]),
        small_movies_count=len([c for c in competitor_list if c.category == "small"]),
        high_threat_count=len([c for c in competitor_list if c.threat_level == "high"]),
        recommendation=analysis["recommendation"],
        optimal_release_windows=analysis["optimal_windows"],
        risk_assessment=analysis["risk_assessment"]
    )

@router.post("/pr-strategy", response_model=PRStrategyResponse)
async def generate_pr_strategy(
    request: PRStrategyRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate AI-powered PR strategy using DeepSeek-R1 based on competitive landscape.
    """
    db = get_database()
    
    # Get the producer's movie
    movie = await db.movies.find_one({"_id": ObjectId(request.movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get competitor data if provided
    competitors_data = []
    if request.competitor_movie_ids:
        for comp_id in request.competitor_movie_ids:
            comp = await db.movies.find_one({"_id": ObjectId(comp_id)})
            if comp:
                competitors_data.append({
                    "title": comp["title"],
                    "category": ReleaseStrategyService.categorize_movie(comp),
                    "genre": comp["genre"],
                    "budget": comp.get("budget", 0),
                    "release_date": comp.get("release_date"),
                    "cast_score": comp.get("cast_score", 0),
                    "historic_score": comp.get("historic_score", 0),
                    "public_pulse_score": comp.get("public_pulse_score", 0)
                })
    
    # Generate PR strategy using DeepSeek
    deepseek_service = DeepSeekService()
    
    movie_category = ReleaseStrategyService.categorize_movie(movie)
    
    pr_strategy = await deepseek_service.generate_pr_strategy(
        movie_data={
            "title": movie["title"],
            "director": movie["director"],
            "genre": movie["genre"],
            "budget": movie.get("budget", 0),
            "category": movie_category,
            "language": movie.get("language", ""),
            "themes": movie.get("themes", ""),
            "region": movie.get("region", ""),
            "cast_score": movie.get("cast_score", 0),
            "historic_score": movie.get("historic_score", 0),
            "public_pulse_score": movie.get("public_pulse_score", 0),
            "release_date": movie.get("release_date")
        },
        competitors=competitors_data,
        focus_areas=request.focus_areas
    )
    
    # Store PR strategy in database
    pr_doc = {
        "movie_id": request.movie_id,
        "producer_id": str(current_user["_id"]),
        "strategy": pr_strategy,
        "created_at": datetime.utcnow()
    }
    await db.pr_strategies.insert_one(pr_doc)
    
    return PRStrategyResponse(
        movie_id=request.movie_id,
        movie_title=movie["title"],
        movie_category=movie_category,
        pr_strategy=pr_strategy["strategy"],
        key_differentiators=pr_strategy["key_differentiators"],
        target_audience_approach=pr_strategy["target_audience"],
        media_channels=pr_strategy["media_channels"],
        timeline=pr_strategy["timeline"],
        budget_allocation=pr_strategy["budget_allocation"],
        risk_mitigation=pr_strategy["risk_mitigation"],
        success_metrics=pr_strategy["success_metrics"]
    )

@router.post("/release-date-decision", response_model=dict)
async def get_release_date_decision(
    request: ReleaseDateAnalysisRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    AI-powered release date decision using DeepSeek-R1.
    Analyzes competitive landscape and recommends optimal release date.
    """
    db = get_database()
    
    # Get the producer's movie
    movie = await db.movies.find_one({"_id": ObjectId(request.movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get date range analysis first
    target_date = request.target_release_date or movie.get("release_date")
    if not target_date:
        raise HTTPException(status_code=400, detail="Release date not set")
    
    days_before = request.days_before or 45
    days_after = request.days_after or 45
    
    start_date = target_date - timedelta(days=days_before)
    end_date = target_date + timedelta(days=days_after)
    
    # Find all movies in extended date range
    competitors = await db.movies.find({
        "_id": {"$ne": ObjectId(request.movie_id)},
        "release_date": {
            "$gte": start_date,
            "$lte": end_date
        },
        "status": {"$in": ["awaiting-release", "released"]}
    }).to_list(100)
    
    # Prepare competitor data
    competitors_data = []
    for comp in competitors:
        competitors_data.append({
            "title": comp["title"],
            "category": ReleaseStrategyService.categorize_movie(comp),
            "genre": comp["genre"],
            "release_date": comp["release_date"],
            "cast_score": comp.get("cast_score", 0),
            "historic_score": comp.get("historic_score", 0),
            "public_pulse_score": comp.get("public_pulse_score", 0),
            "language": comp.get("language", ""),
            "region": comp.get("region", "")
        })
    
    # Use DeepSeek for release date decision
    deepseek_service = DeepSeekService()
    
    decision = await deepseek_service.analyze_release_date(
        movie_data={
            "title": movie["title"],
            "director": movie["director"],
            "genre": movie["genre"],
            "category": ReleaseStrategyService.categorize_movie(movie),
            "language": movie.get("language", ""),
            "region": movie.get("region", ""),
            "target_date": target_date
        },
        competitors=competitors_data,
        date_range=(start_date, end_date)
    )
    
    return {
        "movie_id": request.movie_id,
        "current_target_date": target_date,
        "recommended_date": decision["recommended_date"],
        "confidence_score": decision["confidence_score"],
        "reasoning": decision["reasoning"],
        "alternative_dates": decision["alternative_dates"],
        "competitive_analysis": decision["competitive_analysis"],
        "market_conditions": decision["market_conditions"],
        "action_items": decision["action_items"]
    }
