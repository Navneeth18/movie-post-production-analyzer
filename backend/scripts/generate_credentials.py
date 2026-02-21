"""Generate credentials file for all producers"""
import asyncio
import sys
import re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def generate_credentials():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Get all migrated users
        users = await db.users.find({"is_migrated": True}).sort("full_name", 1).to_list(None)
        
        # Count movies per producer
        producer_movies = {}
        for user in users:
            count = await db.historical_movies.count_documents({"producer_id": str(user["_id"])})
            producer_movies[str(user["_id"])] = count
        
        # Generate credentials file
        credentials_file = Path(__file__).parent / "producer_credentials.txt"
        with open(credentials_file, 'w', encoding='utf-8') as f:
            f.write("PRODUCER LOGIN CREDENTIALS\n")
            f.write("=" * 90 + "\n\n")
            f.write(f"{'Producer Name':<35} {'Email':<40} {'Password':<10} {'Movies'}\n")
            f.write("-" * 90 + "\n")
            
            for user in users:
                name = user.get('full_name', '')
                email = user.get('email', '')
                movie_count = producer_movies.get(str(user["_id"]), 0)
                f.write(f"{name:<35} {email:<40} {'123456':<10} {movie_count}\n")
            
            f.write("\n" + "=" * 90 + "\n")
            f.write(f"\nTotal Accounts: {len(users)}\n")
            f.write(f"Total Movies Linked: {sum(producer_movies.values())}\n")
            f.write(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✓ Credentials saved to: {credentials_file}")
        print(f"\nTotal producers: {len(users)}")
        print(f"Total movies linked: {sum(producer_movies.values())}")
        
        # Show sample
        print("\nSample credentials:")
        print("-" * 90)
        for user in users[:5]:
            name = user.get('full_name', '')
            email = user.get('email', '')
            movie_count = producer_movies.get(str(user["_id"]), 0)
            print(f"{name:<35} {email:<40} 123456     {movie_count}")
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(generate_credentials())
