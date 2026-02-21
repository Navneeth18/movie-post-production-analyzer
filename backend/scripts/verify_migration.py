"""
Script to verify the migration was successful
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def verify_migration():
    """Verify migration results"""
    
    print("\n" + "=" * 60)
    print("MIGRATION VERIFICATION")
    print("=" * 60)
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Check users
        total_users = await db.users.count_documents({})
        migrated_users = await db.users.count_documents({"is_migrated": True})
        
        print(f"\n[USERS]")
        print(f"  Total users: {total_users}")
        print(f"  Migrated producers: {migrated_users}")
        
        # Check historical movies
        total_historical = await db.historical_movies.count_documents({})
        linked_movies = await db.historical_movies.count_documents({"producer_id": {"$exists": True}})
        tagged_movies = await db.historical_movies.count_documents({"tag": "past"})
        
        print(f"\n[HISTORICAL MOVIES]")
        print(f"  Total movies: {total_historical}")
        print(f"  Linked to producers: {linked_movies}")
        print(f"  Tagged as 'past': {tagged_movies}")
        
        # Sample data
        print(f"\n[SAMPLE DATA]")
        sample_user = await db.users.find_one({"is_migrated": True})
        if sample_user:
            print(f"  Sample Producer:")
            print(f"    Name: {sample_user.get('full_name')}")
            print(f"    Email: {sample_user.get('email')}")
            print(f"    Username: {sample_user.get('username')}")
            
            # Count their movies
            user_movies = await db.historical_movies.count_documents({"producer_id": str(sample_user["_id"])})
            print(f"    Movies: {user_movies}")
        
        # Check for issues
        print(f"\n[ISSUES CHECK]")
        movies_without_producer = await db.historical_movies.count_documents({
            "producer_id": {"$exists": False}
        })
        if movies_without_producer > 0:
            print(f"  ⚠ {movies_without_producer} movies without producer_id")
        else:
            print(f"  ✓ All movies have producer_id")
        
        print("\n" + "=" * 60)
        print("✅ Verification complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_migration())
