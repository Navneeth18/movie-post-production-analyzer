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
    
    # Calculate scores using HWS Calculator
    from app.services.hws_calculator import HWSCalculator
    
    # Calculate cast score
    cast_score = await MovieService.calculate_cast_score([c.dict() for c in movie_data.cast])
    
    # Calculate HWS
    hws_result = await HWSCalculator.calculate_hws(
        director=movie_data.director,
        genres=movie_data.genres,
        cast=[c.dict() for c in movie_data.cast],
        producer=current_user.get("full_name"),
        popularity_score=50.0  # Default, will be updated when trailer is added
    )
    
    movie_dict = movie_data.dict()
    movie_dict.update({
        "producer_id": str(current_user["_id"]),
        "cast_score": cast_score,
        "hws_score": hws_result['hws_score'],
        "category": hws_result['category'],
        "market_action": hws_result['market_action'],
        "hws_breakdown": hws_result['breakdown'],
        "tag": "current",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    })
    
    result = await db.movies.insert_one(movie_dict)
    movie_dict["id"] = str(result.inserted_id)
    
    return MovieResponse(**movie_dict)

@router.get("/", response_model=List[dict])
async def get_my_movies(
    include_historical: bool = True,
    current_user: dict = Depends(get_current_user)
):
    """Get all movies for the logged-in producer (current + historical)"""
    db = get_database()
    
    result = []
    
    # Get current movies from 'movies' collection
    current_movies = await db.movies.find({
        "producer_id": str(current_user["_id"])
    }).to_list(100)
    
    for m in current_movies:
        result.append({
            "id": str(m["_id"]),
            "title": m.get("title"),
            "director": m.get("director"),
            "genres": m.get("genres", []),
            "languages": m.get("languages", []),
            "budget": m.get("budget"),
            "release_date": m.get("release_date"),
            "status": m.get("status"),
            "tag": m.get("tag", "current"),
            "cast_score": m.get("cast_score"),
            "hws_score": m.get("hws_score"),
            "category": m.get("category"),
            "market_action": m.get("market_action"),
            "hws_breakdown": m.get("hws_breakdown"),
            "region": m.get("region"),
            "cast": m.get("cast", []),
            "youtube_video_id": m.get("youtube_video_id"),  # Include to show if trailer is linked
            "source": "current"
        })
    
    # Get historical movies from 'historical_movies' collection
    if include_historical:
        from app.services.hws_calculator import HWSCalculator
        
        historical_movies = await db.historical_movies.find({
            "producer_id": str(current_user["_id"]),
            "tag": "past"
        }).to_list(200)
        
        for m in historical_movies:
            # Calculate cast score and HWS using HWS Calculator
            hws_result = await HWSCalculator.calculate_historical_movie_hws(
                director=m.get('director', ''),
                genre=m.get('genre', ''),
                hero=m.get('hero'),
                heroine=m.get('heroine'),
                producer=m.get('producer'),
                budget=m.get('budget', 0),
                revenue=m.get('revenue', 0)
            )
            
            result.append({
                "id": str(m["_id"]),
                "title": m.get("movie_name"),
                "director": m.get("director"),
                "genres": [m.get("genre")] if m.get("genre") else [],
                "languages": [],
                "budget": m.get("budget", 0),
                "revenue": m.get("revenue", 0),
                "release_date": m.get("release_date"),
                "status": "released",
                "tag": "past",
                "imdb_rating": m.get("imdb_rating"),
                "popularity_score": m.get("popularity_score"),
                "hero": m.get("hero"),
                "heroine": m.get("heroine"),
                "cast_score": hws_result['breakdown']['hero_score'],  # Use calculated hero score
                "hws_score": hws_result['hws_score'],
                "category": hws_result['category'],
                "market_action": hws_result['market_action'],
                "hws_breakdown": hws_result['breakdown'],
                "source": "historical"
            })
    
    return result

@router.get("/historical", response_model=List[dict])
async def get_my_historical_movies(current_user: dict = Depends(get_current_user)):
    """Get historical movies for the logged-in producer"""
    db = get_database()
    
    movies = await db.historical_movies.find({
        "producer_id": str(current_user["_id"]),
        "tag": "past"
    }).to_list(200)
    
    return [
        {
            "id": str(m["_id"]),
            "movie_name": m.get("movie_name"),
            "hero": m.get("hero"),
            "heroine": m.get("heroine"),
            "director": m.get("director"),
            "producer": m.get("producer"),
            "budget": m.get("budget", 0),
            "revenue": m.get("revenue", 0),
            "imdb_rating": m.get("imdb_rating", 0),
            "popularity_score": m.get("popularity_score", 0),
            "genre": m.get("genre"),
            "release_date": m.get("release_date"),
            "tag": m.get("tag", "past")
        }
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
    """Get a specific movie by ID (checks both current and historical movies)"""
    db = get_database()
    
    try:
        # First, try to find in current movies collection
        movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
        
        if movie:
            return MovieResponse(id=str(movie["_id"]), **{k: v for k, v in movie.items() if k != "_id"})
        
        # If not found, try historical movies collection
        historical_movie = await db.historical_movies.find_one({"_id": ObjectId(movie_id)})
        
        if historical_movie:
            # Calculate HWS for historical movie
            from app.services.hws_calculator import HWSCalculator
            
            hws_result = await HWSCalculator.calculate_historical_movie_hws(
                director=historical_movie.get('director', ''),
                genre=historical_movie.get('genre', ''),
                hero=historical_movie.get('hero'),
                heroine=historical_movie.get('heroine'),
                producer=historical_movie.get('producer'),
                budget=historical_movie.get('budget', 0),
                revenue=historical_movie.get('revenue', 0)
            )
            
            # Convert historical movie to MovieResponse format
            cast_list = []
            if historical_movie.get("hero"):
                cast_list.append({"name": historical_movie.get("hero"), "role": "Hero"})
            if historical_movie.get("heroine"):
                cast_list.append({"name": historical_movie.get("heroine"), "role": "Heroine"})
            
            # Parse release date if it's a string
            release_date = historical_movie.get("release_date")
            if isinstance(release_date, str):
                try:
                    from datetime import datetime as dt
                    # Try parsing DD-MM-YYYY format
                    release_date = dt.strptime(release_date, "%d-%m-%Y")
                except:
                    release_date = None
            
            movie_data = {
                "id": str(historical_movie["_id"]),
                "title": historical_movie.get("movie_name", "Unknown"),
                "director": historical_movie.get("director", "Unknown"),
                "genres": [historical_movie.get("genre")] if historical_movie.get("genre") else ["Unknown"],
                "languages": [],
                "budget": historical_movie.get("budget"),
                "budget_currency": "INR",
                "release_date": release_date,
                "region": historical_movie.get("region"),
                "cast": cast_list,
                "producer_id": historical_movie.get("producer_id", ""),
                "status": "released",
                "tag": "past",
                "hws_score": hws_result['hws_score'],
                "category": hws_result['category'],
                "market_action": hws_result['market_action'],
                "hws_breakdown": hws_result['breakdown'],
                "cast_score": hws_result['breakdown']['hero_score'],
                "created_at": historical_movie.get("created_at"),
                "updated_at": historical_movie.get("updated_at")
            }
            
            return MovieResponse(**movie_data)
        
        # Not found in either collection
        raise HTTPException(status_code=404, detail="Movie not found")
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_movie: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
    
    # Recalculate cast score if cast changed
    if "cast" in update_data:
        update_data["cast_score"] = await MovieService.calculate_cast_score(update_data["cast"])
    
    # Recalculate HWS if relevant fields changed
    if any(field in update_data for field in ["director", "genres", "cast"]):
        from app.services.hws_calculator import HWSCalculator
        
        director = update_data.get("director", movie["director"])
        genres = update_data.get("genres", movie.get("genres", []))
        cast = update_data.get("cast", movie.get("cast", []))
        
        hws_result = await HWSCalculator.calculate_hws(
            director=director,
            genres=genres,
            cast=cast,
            producer=current_user.get("full_name"),
            popularity_score=movie.get("public_pulse_score", 50.0)
        )
        
        update_data["hws_score"] = hws_result['hws_score']
        update_data["category"] = hws_result['category']
        update_data["market_action"] = hws_result['market_action']
        update_data["hws_breakdown"] = hws_result['breakdown']
    
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
    """Analyze competitor movie (current movies only)"""
    db = get_database()
    
    # Get user's movie
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a current movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400, 
            detail="Competitor analysis is only available for current movies"
        )
    
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
    """Get all competitors for a specific movie (current movies only)"""
    db = get_database()
    
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    # Check if it's a current movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400, 
            detail="Competitor analysis is only available for current movies"
        )
    
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
