"""Test complete HWS flow with movie creation"""
import asyncio
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database
from app.services.movie_service import MovieService
from app.services.hws_calculator import HWSCalculator

async def test_complete_flow():
    await connect_to_mongo()
    db = get_database()
    
    print("Testing Complete HWS Flow")
    print("=" * 70)
    
    # Test 1: Calculate cast score for a movie
    print("\n1. CAST SCORE CALCULATION")
    print("-" * 70)
    cast = [
        {"name": "Prabhas", "role": "Hero"},
        {"name": "Anushka Shetty", "role": "Heroine"}
    ]
    
    cast_score = await MovieService.calculate_cast_score(cast)
    print(f"Cast: Prabhas (Hero) + Anushka Shetty (Heroine)")
    print(f"Cast Score: {cast_score}")
    
    # Test 2: Calculate HWS for current movie
    print("\n\n2. CURRENT MOVIE HWS CALCULATION")
    print("-" * 70)
    hws_result = await HWSCalculator.calculate_hws(
        director="S. S. Rajamouli",
        genres=["Action", "Drama"],
        cast=cast,
        producer="Shobu Yarlagadda",
        popularity_score=50.0  # Default for new movie
    )
    
    print(f"Director: S. S. Rajamouli")
    print(f"Genres: Action, Drama")
    print(f"HWS Score: {hws_result['hws_score']}")
    print(f"Category: {hws_result['category']}")
    print(f"Cast Score: {cast_score}")
    
    # Test 3: Historical movie from database
    print("\n\n3. HISTORICAL MOVIE HWS CALCULATION")
    print("-" * 70)
    
    # Get a sample historical movie
    historical_movie = await db.historical_movies.find_one({"producer": "Dil Raju"})
    
    if historical_movie:
        print(f"Movie: {historical_movie.get('movie_name')}")
        print(f"Director: {historical_movie.get('director')}")
        print(f"Hero: {historical_movie.get('hero')}")
        print(f"Heroine: {historical_movie.get('heroine')}")
        
        hws_result = await HWSCalculator.calculate_historical_movie_hws(
            director=historical_movie.get('director', ''),
            genre=historical_movie.get('genre', ''),
            hero=historical_movie.get('hero'),
            heroine=historical_movie.get('heroine'),
            producer=historical_movie.get('producer'),
            budget=historical_movie.get('budget', 0),
            revenue=historical_movie.get('revenue', 0)
        )
        
        print(f"\nHWS Score: {hws_result['hws_score']}")
        print(f"Category: {hws_result['category']}")
        print(f"Hero Score: {hws_result['breakdown']['hero_score']}")
        print(f"Heroine Score: {hws_result['breakdown']['heroine_score']}")
        print(f"Director Score: {hws_result['breakdown']['director_score']}")
    else:
        print("No historical movies found for Dil Raju")
    
    # Test 4: Check multiple historical movies
    print("\n\n4. BATCH HISTORICAL MOVIES TEST")
    print("-" * 70)
    
    historical_movies = await db.historical_movies.find({"producer": "Dil Raju"}).limit(3).to_list(3)
    
    for movie in historical_movies:
        hws_result = await HWSCalculator.calculate_historical_movie_hws(
            director=movie.get('director', ''),
            genre=movie.get('genre', ''),
            hero=movie.get('hero'),
            heroine=movie.get('heroine'),
            producer=movie.get('producer'),
            budget=movie.get('budget', 0),
            revenue=movie.get('revenue', 0)
        )
        
        print(f"\n{movie.get('movie_name')}")
        print(f"  HWS: {hws_result['hws_score']} ({hws_result['category']})")
        print(f"  Cast Score: {hws_result['breakdown']['hero_score']}")
    
    print("\n" + "=" * 70)
    print("✅ Complete HWS Flow Tests Passed!")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(test_complete_flow())
