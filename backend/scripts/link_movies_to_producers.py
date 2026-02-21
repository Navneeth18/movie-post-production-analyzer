"""Link historical movies to existing producer accounts"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def link_movies():
    """Link movies to producers"""
    
    print("\n" + "=" * 60)
    print("LINKING MOVIES TO PRODUCERS")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Get all users
        print("\n[1/3] Loading producer accounts...")
        users = await db.users.find({"is_migrated": True}).to_list(None)
        
        # Create mapping: producer_name -> user_id
        producer_map = {}
        for user in users:
            producer_map[user['full_name']] = str(user['_id'])
        
        print(f"✓ Loaded {len(producer_map)} producer accounts")
        
        # Get all historical movies
        print("\n[2/3] Loading historical movies...")
        movies = await db.historical_movies.find({}).to_list(None)
        print(f"✓ Found {len(movies)} historical movies")
        
        # Link movies to producers
        print("\n[3/3] Linking movies to producers...")
        updated_count = 0
        no_producer_count = 0
        not_found_count = 0
        
        for movie in movies:
            producer = movie.get('producer')
            
            # Skip if no producer or not a string
            if not producer or not isinstance(producer, str):
                no_producer_count += 1
                continue
            
            producer = producer.strip()
            if not producer:
                no_producer_count += 1
                continue
            
            # Find producer_id
            if producer in producer_map:
                producer_id = producer_map[producer]
                
                # Update movie
                await db.historical_movies.update_one(
                    {"_id": movie["_id"]},
                    {
                        "$set": {
                            "producer_id": producer_id,
                            "tag": "past",
                            "status": "released",
                            "updated_at": datetime.utcnow()
                        }
                    }
                )
                updated_count += 1
                
                if updated_count % 50 == 0:
                    print(f"  Progress: {updated_count} movies linked...")
            else:
                not_found_count += 1
                print(f"  ⚠ Producer not found: {producer}")
        
        print(f"\n✓ Linked {updated_count} movies to producers")
        if no_producer_count > 0:
            print(f"⚠ {no_producer_count} movies have no producer information")
        if not_found_count > 0:
            print(f"⚠ {not_found_count} movies have producers not in user database")
        
        # Verification
        print("\n[VERIFICATION]")
        total_linked = await db.historical_movies.count_documents({"producer_id": {"$exists": True}})
        total_tagged = await db.historical_movies.count_documents({"tag": "past"})
        print(f"✓ Total movies with producer_id: {total_linked}")
        print(f"✓ Total movies tagged as 'past': {total_tagged}")
        
        print("\n" + "=" * 60)
        print("✅ Linking complete!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(link_movies())
