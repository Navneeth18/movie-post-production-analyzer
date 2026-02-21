"""
Create Test Movie for Public Pulse with Competitors
Creates a test movie for dilraju@gmail.com and adds 3-4 competing movies
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import datetime, timedelta
import random
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/film_db')
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test movie release date
TEST_MOVIE_RELEASE = datetime(2026, 3, 15)  # March 15, 2026

# Competitor movies data
COMPETITORS = [
    {
        "title": "Mega Action Hero",
        "director": "S. S. Rajamouli",
        "genres": ["Action", "Drama"],
        "budget": 250000000,  # ₹25Cr - Big movie
        "release_date": datetime(2026, 3, 12),  # 3 days before
        "languages": ["Telugu", "Hindi", "Tamil"],
        "region": "Pan-India",
        "cast": [
            {"name": "Allu Arjun", "role": "Lead 1 (Hero)", "star_power": None},
            {"name": "Rashmika Mandanna", "role": "Lead 2 (Heroine)", "star_power": None}
        ],
        "status": "awaiting-release",
        "producer_name": "Sukumar"
    },
    {
        "title": "Family Drama Special",
        "director": "Trivikram Srinivas",
        "genres": ["Family", "Drama"],
        "budget": 120000000,  # ₹12Cr - Medium movie
        "release_date": datetime(2026, 3, 15),  # Same day!
        "languages": ["Telugu"],
        "region": "Andhra Pradesh",
        "cast": [
            {"name": "Nani", "role": "Lead 1 (Hero)", "star_power": None},
            {"name": "Sai Pallavi", "role": "Lead 2 (Heroine)", "star_power": None}
        ],
        "status": "awaiting-release",
        "producer_name": "BVSN Prasad"
    },
    {
        "title": "Romantic Thriller",
        "director": "Koratala Siva",
        "genres": ["Romance", "Thriller"],
        "budget": 80000000,  # ₹8Cr - Small movie
        "release_date": datetime(2026, 3, 18),  # 3 days after
        "languages": ["Telugu"],
        "region": "Telangana",
        "cast": [
            {"name": "Ram Charan", "role": "Lead 1 (Hero)", "star_power": None},
            {"name": "Samantha Ruth Prabhu", "role": "Lead 2 (Heroine)", "star_power": None}
        ],
        "status": "post-production",
        "producer_name": "Prasad Devineni"
    },
    {
        "title": "Comedy Blockbuster",
        "director": "Prashanth Neel",
        "genres": ["Comedy", "Action"],
        "budget": 180000000,  # ₹18Cr - Medium-Big movie
        "release_date": datetime(2026, 3, 20),  # 5 days after
        "languages": ["Telugu", "Hindi"],
        "region": "South India",
        "cast": [
            {"name": "Prabhas", "role": "Lead 1 (Hero)", "star_power": None},
            {"name": "Kajal Aggarwal", "role": "Lead 2 (Heroine)", "star_power": None}
        ],
        "status": "awaiting-release",
        "producer_name": "Sahu Garapati"
    }
]

async def create_or_get_user(db, email, username, full_name, password="TestUser@123"):
    """Create user if doesn't exist"""
    user = await db.users.find_one({"email": email})
    
    if user:
        print(f"✓ User already exists: {email}")
        return str(user['_id'])
    
    user_doc = {
        "email": email,
        "username": username,
        "full_name": full_name,
        "hashed_password": pwd_context.hash(password),
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_doc)
    print(f"✓ Created user: {email}")
    return str(result.inserted_id)

async def create_test_movie(db, producer_id):
    """Create Test Movie for Public Pulse"""
    # Check if already exists
    existing = await db.movies.find_one({
        "producer_id": producer_id,
        "title": "Test Movie for Public Pulse"
    })
    
    if existing:
        print(f"✓ Test movie already exists: {existing['title']}")
        return str(existing['_id'])
    
    movie_doc = {
        "title": "Test Movie for Public Pulse",
        "director": "Sukumar",
        "genres": ["Action", "Thriller"],
        "budget": 150000000,  # ₹15Cr - Medium movie
        "budget_currency": "INR",
        "release_date": TEST_MOVIE_RELEASE,
        "languages": ["Telugu", "Hindi"],
        "region": "South India",
        "cast": [
            {"name": "Nani", "role": "Lead 1 (Hero)", "star_power": None},
            {"name": "Rashmika Mandanna", "role": "Lead 2 (Heroine)", "star_power": None}
        ],
        "producer_id": producer_id,
        "status": "awaiting-release",
        "tag": "current",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "hws_score": None,
        "cast_score": None,
        "historic_score": None,
        "public_pulse_score": 75.5  # Sample score
    }
    
    result = await db.movies.insert_one(movie_doc)
    print(f"✓ Created test movie: Test Movie for Public Pulse")
    print(f"  Release: {TEST_MOVIE_RELEASE.strftime('%b %d, %Y')}")
    print(f"  Budget: ₹15Cr")
    return str(result.inserted_id)

async def create_competitors(db):
    """Create competitor movies"""
    print("\n" + "="*80)
    print("Creating Competitor Movies")
    print("="*80)
    
    created_count = 0
    
    for comp_data in COMPETITORS:
        # Get producer
        producer = await db.users.find_one({
            "$or": [
                {"full_name": comp_data["producer_name"]},
                {"username": comp_data["producer_name"].lower().replace(" ", "")}
            ]
        })
        
        if not producer:
            print(f"✗ Producer not found: {comp_data['producer_name']}")
            continue
        
        producer_id = str(producer['_id'])
        
        # Check if movie already exists
        existing = await db.movies.find_one({
            "title": comp_data["title"],
            "producer_id": producer_id
        })
        
        if existing:
            print(f"⊘ Already exists: {comp_data['title']}")
            continue
        
        # Create movie
        movie_doc = {
            "title": comp_data["title"],
            "director": comp_data["director"],
            "genres": comp_data["genres"],
            "budget": comp_data["budget"],
            "budget_currency": "INR",
            "release_date": comp_data["release_date"],
            "languages": comp_data["languages"],
            "region": comp_data["region"],
            "cast": comp_data["cast"],
            "producer_id": producer_id,
            "status": comp_data["status"],
            "tag": "current",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "hws_score": None,
            "cast_score": random.randint(60, 95),
            "historic_score": random.randint(65, 90),
            "public_pulse_score": random.randint(70, 95)
        }
        
        await db.movies.insert_one(movie_doc)
        created_count += 1
        
        budget_cr = comp_data["budget"] / 10000000
        days_diff = (comp_data["release_date"] - TEST_MOVIE_RELEASE).days
        timing = f"{abs(days_diff)} days {'before' if days_diff < 0 else 'after' if days_diff > 0 else 'SAME DAY'}"
        
        print(f"✓ {comp_data['title']}")
        print(f"  Producer: {comp_data['producer_name']}")
        print(f"  Release: {comp_data['release_date'].strftime('%b %d, %Y')} ({timing})")
        print(f"  Budget: ₹{budget_cr:.1f}Cr")
        print(f"  Director: {comp_data['director']}")
        print(f"  Cast: {comp_data['cast'][0]['name']} & {comp_data['cast'][1]['name']}")
    
    return created_count

async def main():
    print("\n" + "="*80)
    print("CREATE TEST MOVIE WITH COMPETITORS")
    print("For: dilraju@gmail.com")
    print("="*80)
    
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database()
    
    try:
        # Create or get dilraju@gmail.com user
        print("\nStep 1: Create/Get User")
        print("-" * 80)
        producer_id = await create_or_get_user(
            db,
            email="dilraju@gmail.com",
            username="dilrajugmail",
            full_name="Dil Raju (Gmail)",
            password="TestUser@123"
        )
        
        # Create test movie
        print("\nStep 2: Create Test Movie")
        print("-" * 80)
        test_movie_id = await create_test_movie(db, producer_id)
        
        # Create competitors
        print("\nStep 3: Create Competitors")
        competitors_created = await create_competitors(db)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ User: dilraju@gmail.com")
        print(f"✓ Password: TestUser@123")
        print(f"✓ Test Movie: Test Movie for Public Pulse")
        print(f"✓ Release Date: {TEST_MOVIE_RELEASE.strftime('%b %d, %Y')}")
        print(f"✓ Competitors Created: {competitors_created}")
        print("\nCompetitor Timeline:")
        print(f"  Mar 12 (3 days before): Mega Action Hero (₹25Cr - BIG)")
        print(f"  Mar 15 (SAME DAY):      Family Drama Special (₹12Cr - MEDIUM)")
        print(f"  Mar 15 (YOUR MOVIE):    Test Movie for Public Pulse (₹15Cr - MEDIUM)")
        print(f"  Mar 18 (3 days after):  Romantic Thriller (₹8Cr - SMALL)")
        print(f"  Mar 20 (5 days after):  Comedy Blockbuster (₹18Cr - MEDIUM-BIG)")
        print("\nLogin Details:")
        print("  URL: http://localhost:5173/login")
        print("  Email: dilraju@gmail.com")
        print("  Password: TestUser@123")
        print("\nNext Steps:")
        print("  1. Login with above credentials")
        print("  2. Go to 'My Movies'")
        print("  3. Select 'Test Movie for Public Pulse'")
        print("  4. Use 'Release Strategy' to see competitors")
        print("="*80)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
