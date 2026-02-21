"""Debug historical movies for a specific producer"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def debug_producer(email):
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Find user
        user = await db.users.find_one({"email": email})
        if not user:
            print(f"❌ User not found: {email}")
            return
        
        print(f"✓ Found user:")
        print(f"  Name: {user.get('full_name')}")
        print(f"  Email: {user.get('email')}")
        print(f"  ID: {user['_id']}")
        
        # Find historical movies
        user_id = str(user['_id'])
        movies = await db.historical_movies.find({"producer_id": user_id}).to_list(None)
        
        print(f"\n✓ Historical movies: {len(movies)}")
        
        if len(movies) > 0:
            print("\nMovies:")
            for movie in movies:
                print(f"  - {movie.get('movie_name')}")
                print(f"    Producer: {movie.get('producer')}")
                print(f"    Producer ID: {movie.get('producer_id')}")
                print(f"    Tag: {movie.get('tag')}")
                print()
        else:
            print("\n⚠ No historical movies found for this producer")
            
            # Check if movies exist with producer name
            producer_name = user.get('full_name')
            movies_by_name = await db.historical_movies.find({"producer": producer_name}).to_list(None)
            print(f"\nMovies with producer name '{producer_name}': {len(movies_by_name)}")
            
            if len(movies_by_name) > 0:
                print("These movies exist but are not linked!")
                for movie in movies_by_name[:3]:
                    print(f"  - {movie.get('movie_name')}")
                    print(f"    Has producer_id: {'producer_id' in movie}")
                    print(f"    Producer_id value: {movie.get('producer_id')}")
                    print()
    
    finally:
        client.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        email = sys.argv[1]
    else:
        # Default test
        email = "prasaddevineni@gmail.com"
    
    print(f"Debugging producer: {email}\n")
    asyncio.run(debug_producer(email))
