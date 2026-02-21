"""Quick check of historical movies data"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def check_data():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Count total movies
        total = await db.historical_movies.count_documents({})
        print(f"Total historical movies: {total}")
        
        # Count movies with producer_id
        with_producer = await db.historical_movies.count_documents({"producer_id": {"$exists": True}})
        print(f"Movies with producer_id: {with_producer}")
        
        # Count movies without producer_id
        without_producer = await db.historical_movies.count_documents({"producer_id": {"$exists": False}})
        print(f"Movies without producer_id: {without_producer}")
        
        # Sample movie
        sample = await db.historical_movies.find_one({})
        if sample:
            print(f"\nSample movie:")
            print(f"  Movie: {sample.get('movie_name')}")
            print(f"  Producer: {sample.get('producer')}")
            print(f"  Has producer_id: {'producer_id' in sample}")
            print(f"  Has tag: {'tag' in sample}")
        
        # Get unique producers
        pipeline = [
            {"$group": {"_id": "$producer"}},
            {"$match": {"_id": {"$ne": None, "$ne": ""}}},
            {"$sort": {"_id": 1}}
        ]
        producers = await db.historical_movies.aggregate(pipeline).to_list(None)
        print(f"\nUnique producers: {len(producers)}")
        if len(producers) > 0:
            print(f"Sample producers: {[p['_id'] for p in producers[:5]]}")
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_data())
