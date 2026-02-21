"""
Script to migrate historical movies and create producer accounts
- Creates user accounts for all producers in historical_movies collection
- Links historical movies to their producer accounts
- Sets default email as producername@gmail.com (no spaces)
- Sets default password as "123456"
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from motor.motor_asyncio import AsyncIOMotorClient
from app.services.auth_service import get_password_hash
from datetime import datetime
import re

# MongoDB connection
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def migrate_historical_movies():
    """Main migration function"""
    
    print("=" * 60)
    print("HISTORICAL MOVIES MIGRATION SCRIPT")
    print("=" * 60)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        # Step 1: Get all unique producers from historical_movies
        print("\n[1/5] Fetching historical movies...")
        historical_movies = await db.historical_movies.find({}).to_list(None)
        print(f"✓ Found {len(historical_movies)} historical movies")
        
        # Extract unique producers
        producers = set()
        for movie in historical_movies:
            producer = movie.get('producer')
            # Skip if producer is None, empty, or NaN
            if producer and isinstance(producer, str) and producer.strip():
                producers.add(producer.strip())
        
        print(f"✓ Found {len(producers)} unique producers")
        
        # Step 2: Create user accounts for producers
        print("\n[2/5] Creating producer accounts...")
        created_users = {}
        skipped_users = []
        
        for producer_name in sorted(producers):
            # Generate email: remove spaces and special chars, lowercase
            username = re.sub(r'[^a-zA-Z0-9]', '', producer_name).lower()
            email = f"{username}@gmail.com"
            
            # Check if user already exists
            existing_user = await db.users.find_one({"email": email})
            if existing_user:
                print(f"  ⊙ Skipped: {producer_name} (email already exists)")
                created_users[producer_name] = str(existing_user["_id"])
                skipped_users.append(producer_name)
                continue
            
            # Create user account
            user_doc = {
                "email": email,
                "username": username,
                "full_name": producer_name,
                "hashed_password": get_password_hash("123456"),
                "is_active": True,
                "created_at": datetime.utcnow(),
                "is_migrated": True  # Flag to identify migrated accounts
            }
            
            result = await db.users.insert_one(user_doc)
            created_users[producer_name] = str(result.inserted_id)
            print(f"  ✓ Created: {producer_name} → {email}")
        
        print(f"\n✓ Created {len(created_users) - len(skipped_users)} new producer accounts")
        print(f"✓ Skipped {len(skipped_users)} existing accounts")
        
        # Step 3: Update historical movies with producer_id
        print("\n[3/5] Linking movies to producers...")
        updated_count = 0
        no_producer_count = 0
        
        for movie in historical_movies:
            producer = movie.get('producer')
            
            # Skip if producer is None, empty, or not a string
            if not producer or not isinstance(producer, str):
                no_producer_count += 1
                continue
            
            producer = producer.strip()
            if not producer:
                no_producer_count += 1
                continue
            
            if producer in created_users:
                producer_id = created_users[producer]
                
                # Update movie with producer_id and tag
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
        
        print(f"✓ Linked {updated_count} movies to producers")
        if no_producer_count > 0:
            print(f"⚠ {no_producer_count} movies have no producer information")
        
        # Step 4: Generate summary report
        print("\n[4/5] Generating summary report...")
        
        # Count movies per producer
        producer_movie_counts = {}
        for movie in historical_movies:
            producer = movie.get('producer', '').strip()
            if producer:
                producer_movie_counts[producer] = producer_movie_counts.get(producer, 0) + 1
        
        # Step 5: Display results
        print("\n[5/5] Migration Complete!")
        print("=" * 60)
        print("\nPRODUCER ACCOUNTS CREATED:")
        print("-" * 60)
        print(f"{'Producer Name':<30} {'Email':<35} {'Movies'}")
        print("-" * 60)
        
        for producer_name in sorted(created_users.keys()):
            username = re.sub(r'[^a-zA-Z0-9]', '', producer_name).lower()
            email = f"{username}@gmail.com"
            movie_count = producer_movie_counts.get(producer_name, 0)
            print(f"{producer_name:<30} {email:<35} {movie_count}")
        
        print("-" * 60)
        print(f"\nTOTAL PRODUCERS: {len(created_users)}")
        print(f"TOTAL MOVIES LINKED: {updated_count}")
        print(f"\nDEFAULT PASSWORD FOR ALL ACCOUNTS: 123456")
        print("\n" + "=" * 60)
        
        # Save credentials to file
        print("\n[BONUS] Saving credentials to file...")
        credentials_file = Path(__file__).parent / "producer_credentials.txt"
        with open(credentials_file, 'w') as f:
            f.write("PRODUCER LOGIN CREDENTIALS\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"{'Producer Name':<30} {'Email':<35} {'Password'}\n")
            f.write("-" * 80 + "\n")
            
            for producer_name in sorted(created_users.keys()):
                username = re.sub(r'[^a-zA-Z0-9]', '', producer_name).lower()
                email = f"{username}@gmail.com"
                f.write(f"{producer_name:<30} {email:<35} 123456\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write(f"\nTotal Accounts: {len(created_users)}\n")
            f.write(f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        print(f"✓ Credentials saved to: {credentials_file}")
        
        # Verification
        print("\n[VERIFICATION]")
        total_users = await db.users.count_documents({})
        total_historical = await db.historical_movies.count_documents({"tag": "past"})
        print(f"✓ Total users in database: {total_users}")
        print(f"✓ Total historical movies tagged: {total_historical}")
        
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()
        print("\n✓ Database connection closed")

if __name__ == "__main__":
    print("\nStarting migration...")
    print("Make sure MongoDB is running!\n")
    
    asyncio.run(migrate_historical_movies())
    
    print("\n✅ Migration script completed!")
    print("\nYou can now:")
    print("  1. Login with any producer email and password '123456'")
    print("  2. View their historical movies in the dashboard")
    print("  3. Check producer_credentials.txt for all login details\n")
