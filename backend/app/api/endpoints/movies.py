from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from bson import ObjectId
from app.schemas.movie_schema import (
    MovieCreate, MovieUpdate, MovieResponse, 
    CompetitorRequest, CompetitorAnalysisResponse
)
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.services.movie_service import MovieService
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie_data: MovieCreate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    # Calculate scores
    cast_score = MovieService.calculate_cast_score([c.dict() for c in movie_data.cast])
    historic_score = MovieService.calculate_historic_score(movie_data.director, movie_data.genre)
    pulse_score = await MovieService.calculate_public_pulse(movie_data.title, movie_data.themes or "")
    
    movie_dict = movie_data.dict()
    movie_dict.update({
        "producer_id": str(current_user["_id"]),
        "cast_score": cast_score,
        "historic_score": historic_score,
        "public_pulse_score": pulse_score,
        "hws_score": None,  # Calculate separately if needed
        "tag": "current",  # Mark as current movie
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db.movies.insert_one(movie_dict)
    movie_dict["id"] = str(result.inserted_id)
    
    return MovieResponse(**movie_dict)

@router.get("/", response_model=List[MovieResponse])
async def get_my_movies(current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    movies = await db.movies.find({
        "producer_id": str(current_user["_id"]),
        "tag": "current"
    }).to_list(100)
    
    return [
        MovieResponse(id=str(m["_id"]), **{k: v for k, v in m.items() if k != "_id"})
        for m in movies
    ]

@router.get("/all", response_model=List[MovieResponse])
async def get_all_movies(
    tag: str = "current",
    current_user: dict = Depends(get_current_user)
):
    """Get all movies in the system (for competitor analysis)"""
    db = get_database()
    
    query = {"tag": tag}
    if tag == "current":
        query["status"] = {"$in": ["awaiting-release", "released"]}
    
    movies = await db.movies.find(query).to_list(200)
    
    return [
        MovieResponse(id=str(m["_id"]), **{k: v for k, v in m.items() if k != "_id"})
        for m in movies
    ]

@router.get("/{movie_id}", response_model=MovieResponse)
async def get_movie(movie_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    return MovieResponse(id=str(movie["_id"]), **{k: v for k, v in movie.items() if k != "_id"})

@router.put("/{movie_id}", response_model=MovieResponse)
async def update_movie(
    movie_id: str,
    movie_data: MovieUpdate,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to update this movie")
    
    update_data = {k: v for k, v in movie_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    # Recalculate scores if relevant fields changed
    if "cast" in update_data:
        update_data["cast_score"] = MovieService.calculate_cast_score(update_data["cast"])
    if "director" in update_data or "genre" in update_data:
        update_data["historic_score"] = MovieService.calculate_historic_score(
            update_data.get("director", movie["director"]),
            update_data.get("genre", movie["genre"])
        )
    
    # If status changes to "released", update tag to "past"
    if update_data.get("status") == "released":
        update_data["tag"] = "past"
    
    await db.movies.update_one({"_id": ObjectId(movie_id)}, {"$set": update_data})
    
    updated_movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    return MovieResponse(id=str(updated_movie["_id"]), **{k: v for k, v in updated_movie.items() if k != "_id"})

@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movie(movie_id: str, current_user: dict = Depends(get_current_user)):
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized to delete this movie")
    
    await db.movies.delete_one({"_id": ObjectId(movie_id)})
    return None

@router.post("/{movie_id}/analyze-competitor", response_model=CompetitorAnalysisResponse)
async def analyze_competitor(
    movie_id: str,
    competitor_data: CompetitorRequest,
    current_user: dict = Depends(get_current_user)
):
    db = get_database()
    
    # Get user's movie
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get competitor movie
    competitor = await db.movies.find_one({"_id": ObjectId(competitor_data.competitor_movie_id)})
    if not competitor:
        raise HTTPException(status_code=404, detail="Competitor movie not found")
    
    # Calculate comparison
    comparison = MovieService.compare_movies(movie, competitor)
    
    # Calculate release date proximity
    days_apart = MovieService.calculate_release_date_proximity(
        movie.get("release_date"),
        competitor.get("release_date")
    )
    
    release_conflict = days_apart < 14  # Within 2 weeks
    
    # Store competitor relationship
    competitor_doc = {
        "movie_id": movie_id,
        "competitor_movie_id": competitor_data.competitor_movie_id,
        "release_date_proximity": days_apart,
        "strength_comparison": comparison["overall_strength"],
        "created_at": datetime.utcnow()
    }
    await db.competitors.insert_one(competitor_doc)
    
    return CompetitorAnalysisResponse(
        movie_id=movie_id,
        competitor_movie_id=competitor_data.competitor_movie_id,
        your_movie_title=movie["title"],
        competitor_movie_title=competitor["title"],
        your_cast_score=movie.get("cast_score", 0),
        competitor_cast_score=competitor.get("cast_score", 0),
        your_historic_score=movie.get("historic_score", 0),
        competitor_historic_score=competitor.get("historic_score", 0),
        your_pulse_score=movie.get("public_pulse_score", 0),
        competitor_pulse_score=competitor.get("public_pulse_score", 0),
        overall_strength=comparison["overall_strength"],
        recommendation=comparison["recommendation"],
        release_date_conflict=release_conflict,
        days_apart=days_apart
    )

@router.get("/{movie_id}/competitors", response_model=List[CompetitorAnalysisResponse])
async def get_movie_competitors(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get all competitors for a specific movie"""
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    competitors = await db.competitors.find({"movie_id": movie_id}).to_list(100)
    
    results = []
    for comp in competitors:
        competitor_movie = await db.movies.find_one({"_id": ObjectId(comp["competitor_movie_id"])})
        if competitor_movie:
            comparison = MovieService.compare_movies(movie, competitor_movie)
            results.append(CompetitorAnalysisResponse(
                movie_id=movie_id,
                competitor_movie_id=comp["competitor_movie_id"],
                your_movie_title=movie["title"],
                competitor_movie_title=competitor_movie["title"],
                your_cast_score=movie.get("cast_score", 0),
                competitor_cast_score=competitor_movie.get("cast_score", 0),
                your_historic_score=movie.get("historic_score", 0),
                competitor_historic_score=competitor_movie.get("historic_score", 0),
                your_pulse_score=movie.get("public_pulse_score", 0),
                competitor_pulse_score=competitor_movie.get("public_pulse_score", 0),
                overall_strength=comparison["overall_strength"],
                recommendation=comparison["recommendation"],
                release_date_conflict=comp["release_date_proximity"] < 14,
                days_apart=comp["release_date_proximity"]
            ))
    
    return results
