"""
Verify Producers in Database
Quick script to check which producers exist and their details
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/film_db')

# Expected producers from credentials file
EXPECTED_PRODUCERS = [
    "Sukumar",
    "Dil Raju", 
    "Sahu Garapati",
    "Prasad Devineni",
    "BVSN Prasad",
    "Rajiv Chilaka",
    "Boddu Koteswara Rao",
    "Vijay Donkada",
    "Suresh Patil",
    "Abhishek Agarwal",
    "Sushmita Konidela"
]

async def verify_producers():
    """Check which producers exist in database"""
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database()
    
    try:
        print("\n" + "="*80)
        print("PRODUCER VERIFICATION")
        print("="*80)
        
        # Get all users
        all_users = await db.users.find({}).to_list(length=100)
        print(f"\nTotal users in database: {len(all_users)}")
        
        print("\n" + "-"*80)
        print("ALL USERS:")
        print("-"*80)
        for i, user in enumerate(all_users, 1):
            print(f"{i}. {user.get('full_name', 'N/A')}")
            print(f"   Email: {user.get('email', 'N/A')}")
            print(f"   Username: {user.get('username', 'N/A')}")
            print(f"   ID: {str(user['_id'])}")
            
            # Check if they have movies
            movie_count = await db.movies.count_documents({"producer_id": str(user['_id'])})
            print(f"   Movies: {movie_count}")
            print()
        
        print("\n" + "-"*80)
        print("EXPECTED PRODUCERS CHECK:")
        print("-"*80)
        
        found_count = 0
        missing_count = 0
        
        for producer_name in EXPECTED_PRODUCERS:
            # Try different username formats
            producer = await db.users.find_one({
                "$or": [
                    {"full_name": producer_name},
                    {"username": producer_name.lower().replace(" ", "")},
                    {"username": producer_name.lower().replace(" ", "_")}
                ]
            })
            
            if producer:
                found_count += 1
                movie_count = await db.movies.count_documents({"producer_id": str(producer['_id'])})
                print(f"✓ FOUND: {producer_name}")
                print(f"  Email: {producer.get('email')}")
                print(f"  Username: {producer.get('username')}")
                print(f"  Movies: {movie_count}")
            else:
                missing_count += 1
                print(f"✗ MISSING: {producer_name}")
                print(f"  Expected usernames: {producer_name.lower().replace(' ', '')}, {producer_name.lower().replace(' ', '_')}")
            print()
        
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"Expected producers: {len(EXPECTED_PRODUCERS)}")
        print(f"Found: {found_count}")
        print(f"Missing: {missing_count}")
        
        if missing_count > 0:
            print("\n⚠ Some producers are missing!")
            print("Please register these producers first using the credentials from:")
            print("backend/scripts/producer_credentials.txt")
        else:
            print("\n✓ All expected producers found!")
        
        print("="*80)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_producers())
