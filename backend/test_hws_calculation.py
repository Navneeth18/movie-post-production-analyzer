"""Test HWS Calculation with real artist data"""
import asyncio
from app.services.hws_calculator import HWSCalculator
from app.db.mongodb import connect_to_mongo, close_mongo_connection

async def test_hws():
    # Initialize database connection
    await connect_to_mongo()
    
    print("Testing HWS Calculation")
    print("=" * 70)
    
    # Test Case 1: Big Movie (Grade 1 Director + Grade 1 Hero)
    print("\n1. BIG MOVIE TEST")
    print("-" * 70)
    result = await HWSCalculator.calculate_hws(
        director="S. S. Rajamouli",  # Should be Grade 1
        genres=["Action", "Drama"],
        cast=[
            {"name": "Prabhas", "role": "Hero"},
            {"name": "Anushka Shetty", "role": "Heroine"}
        ],
        producer="Shobu Yarlagadda",
        popularity_score=85.0
    )
    
    print(f"HWS Score: {result['hws_score']}")
    print(f"Category: {result['category']}")
    print(f"Market Action: {result['market_action']}")
    print("\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # Test Case 2: Medium Movie (Grade 2 Director + Grade 2 Hero)
    print("\n\n2. MEDIUM MOVIE TEST")
    print("-" * 70)
    result = await HWSCalculator.calculate_hws(
        director="Trivikram Srinivas",  # Should be Grade 2
        genres=["Comedy", "Drama"],
        cast=[
            {"name": "Allu Arjun", "role": "Hero"},
            {"name": "Pooja Hegde", "role": "Heroine"}
        ],
        producer="S. Radha Krishna",
        popularity_score=65.0
    )
    
    print(f"HWS Score: {result['hws_score']}")
    print(f"Category: {result['category']}")
    print(f"Market Action: {result['market_action']}")
    print("\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # Test Case 3: Small Movie (Grade 3 Director + Grade 3 Hero)
    print("\n\n3. SMALL MOVIE TEST")
    print("-" * 70)
    result = await HWSCalculator.calculate_hws(
        director="Unknown Director",  # Will default to Grade 3
        genres=["Romance"],
        cast=[
            {"name": "New Actor", "role": "Hero"},
            {"name": "New Actress", "role": "Heroine"}
        ],
        producer="New Producer",
        popularity_score=40.0
    )
    
    print(f"HWS Score: {result['hws_score']}")
    print(f"Category: {result['category']}")
    print(f"Market Action: {result['market_action']}")
    print("\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    # Test Case 4: Historical Movie
    print("\n\n4. HISTORICAL MOVIE TEST")
    print("-" * 70)
    result = await HWSCalculator.calculate_historical_movie_hws(
        director="S. S. Rajamouli",
        genre="Action",
        hero="Prabhas",
        heroine="Anushka Shetty",
        producer="Shobu Yarlagadda",
        budget=180000000,
        revenue=6500000000
    )
    
    print(f"HWS Score: {result['hws_score']}")
    print(f"Category: {result['category']}")
    print(f"Market Action: {result['market_action']}")
    print("\nBreakdown:")
    for key, value in result['breakdown'].items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("✅ HWS Calculation Tests Complete!")
    
    # Close database connection
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(test_hws())
