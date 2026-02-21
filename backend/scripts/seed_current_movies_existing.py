"""
Seed Current Movies for EXISTING Producers
Uses existing producer accounts from database
Creates movies for specific producers with release dates in Feb 23 - March 29, 2026
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

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/film_db')

# Release date range: Feb 23, 2026 to March 29, 2026
RELEASE_START = datetime(2026, 2, 23)
RELEASE_END = datetime(2026, 3, 29)

# EXISTING PRODUCERS (must match database exactly)
# These are from producer_credentials.txt
PRODUCERS = [
    "Sukumar",           # Grade 1 Producer
    "Dil Raju",          # Grade 1 Producer
    "BVSN Prasad",       # Grade 2 Producer
    "Prasad Devineni",   # Grade 2 Producer
    "Sahu Garapati"      # Grade 2 Producer
]

# EXISTING DIRECTORS
DIRECTORS = ["Trivikram Srinivas", "S. S. Rajamouli", "Sukumar", "Koratala Siva", "Prashanth Neel"]

# EXISTING LEAD ACTORS
LEAD1_ACTORS = ["Allu Arjun", "Nani", "S. S. Rajamouli", "Kajal Aggarwal", "Ram Charan"]
LEAD2_ACTORS = ["Sai Pallavi", "Rashmika Mandanna", "Prabhas", "N.T. Rama Rao Jr.", "Samantha Ruth Prabhu"]

# Movie title templates
MOVIE_TITLES = [
    "The Legend", "Warrior", "Rebel", "Champion", "Victory", "Hero", "Fighter",
    "King", "Emperor", "Samrat", "Yodha", "Ravan", "Vikram", "Arjun",
    "Love Story", "Heart Beat", "Romance", "Dream", "Destiny", "Forever",
    "Thriller", "Chase", "Hunt", "Mission", "Target", "Strike",
    "Family", "Home", "Together", "Bond", "Reunion",
    "City Lights", "Street", "Midnight", "Dawn", "Dusk",
    "Power", "Force", "Impact", "Storm", "Thunder"
]

GENRES_LIST = [
    ["Action", "Drama"],
    ["Action", "Thriller"],
    ["Romance", "Drama"],
    ["Comedy", "Romance"],
    ["Thriller", "Mystery"],
    ["Action"],
    ["Drama"],
    ["Comedy"],
    ["Family", "Drama"],
    ["Action", "Comedy"]
]

LANGUAGES_LIST = [
    ["Telugu"],
    ["Telugu", "Hindi"],
    ["Telugu", "Tamil"],
    ["Telugu", "Hindi", "Tamil"],
]

REGIONS = [
    "Andhra Pradesh",
    "Telangana",
    "Hyderabad",
    "South India",
    "Pan-India"
]

STATUSES = ["awaiting-release", "post-production"]

# Budget ranges based on director
BUDGET_RANGES = {
    "S. S. Rajamouli": (200000000, 300000000),  # ₹20-30Cr
    "Prashanth Neel": (150000000, 250000000),   # ₹15-25Cr
    "Koratala Siva": (100000000, 180000000),    # ₹10-18Cr
    "Trivikram Srinivas": (80000000, 150000000), # ₹8-15Cr
    "Sukumar": (100000000, 180000000),          # ₹10-18Cr
}

def generate_release_dates(count):
    """Generate release dates between Feb 23 and March 29, 2026"""
    total_days = (RELEASE_END - RELEASE_START).days
    dates = []
    for _ in range(count):
        random_days = random.randint(0, total_days)
        release_date = RELEASE_START + timedelta(days=random_days)
        dates.append(release_date)
    dates.sort()
    return dates

async def list_all_users(db):
    """Debug: List all users in database"""
    print("\n" + "="*80)
    print("DEBUG: All Users in Database")
    print("="*80)
    
    users = await db.users.find({}).to_list(length=100)
    
    if not users:
        print("No users found in database!")
        return
    
    print(f"Total users: {len(users)}\n")
    for i, user in enumerate(users, 1):
        print(f"{i}. {user.get('full_name', 'N/A')}")
        print(f"   Email: {user.get('email', 'N/A')}")
        print(f"   Username: {user.get('username', 'N/A')}")
        print(f"   ID: {str(user['_id'])}")
        print()

async def get_existing_producers(db):
    """Get existing producer accounts from database"""
    print("\n" + "="*80)
    print("Finding Existing Producer Accounts")
    print("="*80)
    
    producer_map = {}
    producer_details = []
    
    for producer_name in PRODUCERS:
        # Try to find by full_name or username (without role filter)
        producer = await db.users.find_one({
            "$or": [
                {"full_name": producer_name},
                {"username": producer_name.lower().replace(" ", "")},
                {"username": producer_name.lower().replace(" ", "_")}
            ]
        })
        
        if producer:
            producer_map[producer_name] = str(producer['_id'])
            producer_details.append({
                'name': producer_name,
                'email': producer.get('email', 'N/A'),
                'username': producer.get('username', 'N/A'),
                'id': str(producer['_id'])
            })
            print(f"✓ Found: {producer_name}")
            print(f"  Email: {producer.get('email')}")
            print(f"  Username: {producer.get('username')}")
            print(f"  ID: {str(producer['_id'])}")
        else:
            print(f"✗ NOT FOUND: {producer_name}")
            print(f"  Tried usernames: {producer_name.lower().replace(' ', '')}, {producer_name.lower().replace(' ', '_')}")
            print(f"  Please verify this producer exists in the database!")
    
    return producer_map, producer_details

async def clean_duplicate_movies(db, producer_map):
    """Remove movies that were created for wrong producer IDs"""
    print("\n" + "="*80)
    print("Cleaning Duplicate Movies")
    print("="*80)
    
    # Get all producer IDs (both correct and potentially wrong ones)
    all_producer_ids = set(producer_map.values())
    
    # Find all movies with tag="current"
    all_current_movies = await db.movies.find({"tag": "current"}).to_list(length=1000)
    
    print(f"Found {len(all_current_movies)} current movies in database")
    
    # Group movies by producer_id
    movies_by_producer = {}
    for movie in all_current_movies:
        pid = movie.get('producer_id')
        if pid not in movies_by_producer:
            movies_by_producer[pid] = []
        movies_by_producer[pid].append(movie)
    
    print(f"\nMovies grouped by {len(movies_by_producer)} different producer IDs:")
    
    deleted_count = 0
    for pid, movies in movies_by_producer.items():
        # Check if this producer ID is in our valid list
        is_valid = pid in all_producer_ids
        status = "✓ VALID" if is_valid else "✗ INVALID (will delete)"
        
        # Try to find producer name
        producer = await db.users.find_one({"_id": pid})
        producer_name = producer.get('full_name', 'Unknown') if producer else 'Not Found'
        
        print(f"\n{status} Producer: {producer_name} (ID: {pid})")
        print(f"  Movies: {len(movies)}")
        
        # If invalid producer ID, delete these movies
        if not is_valid:
            for movie in movies:
                await db.movies.delete_one({"_id": movie['_id']})
                deleted_count += 1
                print(f"    ✗ Deleted: {movie.get('title')}")
    
    print(f"\n✓ Cleaned up {deleted_count} duplicate/invalid movies")
    return deleted_count

async def create_movies(db, producer_map):
    """Create current movie projects for existing producers"""
    print("\n" + "="*80)
    print("Creating Current Movie Projects")
    print("Release Window: Feb 23, 2026 - March 29, 2026")
    print("="*80)
    
    if not producer_map:
        print("✗ No producers found! Please create producer accounts first.")
        return 0
    
    # Generate 16 movie combinations (3-4 per producer)
    movies_per_producer = {
        producer: [] for producer in producer_map.keys()
    }
    
    # Distribute movies evenly
    total_movies = 16
    producers_list = list(producer_map.keys())
    
    for i in range(total_movies):
        producer = producers_list[i % len(producers_list)]
        movies_per_producer[producer].append(i)
    
    # Generate release dates
    release_dates = generate_release_dates(total_movies)
    
    movies_created = 0
    movie_index = 0
    
    for producer_name, movie_indices in movies_per_producer.items():
        producer_id = producer_map[producer_name]
        
        print(f"\n{producer_name} - Creating {len(movie_indices)} movies:")
        print("-" * 80)
        
        for _ in movie_indices:
            # Generate movie details
            title_base = random.choice(MOVIE_TITLES)
            title_suffix = random.choice(["", " Returns", " 2.0", " Reborn", " Rising", ""])
            title = f"{title_base}{title_suffix}"
            
            director = random.choice(DIRECTORS)
            hero = random.choice(LEAD1_ACTORS)
            heroine = random.choice(LEAD2_ACTORS)
            
            # Get budget range for director
            budget_range = BUDGET_RANGES.get(director, (50000000, 100000000))
            budget = random.randint(budget_range[0], budget_range[1])
            
            genres = random.choice(GENRES_LIST)
            languages = random.choice(LANGUAGES_LIST)
            region = random.choice(REGIONS)
            status = random.choice(STATUSES)
            release_date = release_dates[movie_index]
            movie_index += 1
            
            # Check if movie already exists
            existing = await db.movies.find_one({
                "title": title,
                "producer_id": producer_id
            })
            
            if existing:
                print(f"  ⊘ Already exists: {title}")
                continue
            
            # Create movie document
            movie_doc = {
                "title": title,
                "director": director,
                "genres": genres,
                "budget": budget,
                "budget_currency": "INR",
                "release_date": release_date,
                "languages": languages,
                "region": region,
                "cast": [
                    {
                        "name": hero,
                        "role": "Lead 1 (Hero)",
                        "star_power": None
                    },
                    {
                        "name": heroine,
                        "role": "Lead 2 (Heroine)",
                        "star_power": None
                    }
                ],
                "producer_id": producer_id,
                "status": status,
                "tag": "current",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "hws_score": None,
                "cast_score": None,
                "historic_score": None,
                "public_pulse_score": None
            }
            
            await db.movies.insert_one(movie_doc)
            movies_created += 1
            
            budget_cr = budget / 10000000
            release_str = release_date.strftime('%b %d, %Y')
            print(f"  ✓ {title}")
            print(f"    Release: {release_str}")
            print(f"    Director: {director}")
            print(f"    Cast: {hero} & {heroine}")
            print(f"    Budget: ₹{budget_cr:.1f}Cr | Status: {status}")
    
    return movies_created

def save_producer_info(producer_details):
    """Save producer information to text file"""
    print("\n" + "="*80)
    print("Saving Producer Information")
    print("="*80)
    
    credentials_file = Path(__file__).parent / "existing_producers_info.txt"
    
    with open(credentials_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("EXISTING PRODUCER ACCOUNTS\n")
        f.write("Film Intel Platform - Current Movie Projects\n")
        f.write("Competitive Release Window: Feb 23 - March 29, 2026\n")
        f.write("="*80 + "\n\n")
        
        f.write("LOGIN URL: http://localhost:5173/login\n\n")
        
        f.write("PRODUCERS WITH NEW MOVIES:\n")
        f.write("-" * 80 + "\n")
        for i, prod in enumerate(producer_details, 1):
            f.write(f"{i}. {prod['name']}\n")
            f.write(f"   Email: {prod['email']}\n")
            f.write(f"   Username: {prod['username']}\n")
            f.write(f"   Database ID: {prod['id']}\n\n")
        
        f.write("="*80 + "\n")
        f.write("NOTES:\n")
        f.write("- These are EXISTING producer accounts\n")
        f.write("- Movies are assigned to these existing accounts\n")
        f.write("- All movies release between Feb 23 - March 29, 2026\n")
        f.write("- Login with the existing credentials for these producers\n")
        f.write("- Each producer has 3-4 current movie projects\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Information saved to: {credentials_file}")

async def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("SEED MOVIES FOR EXISTING PRODUCERS")
    print("Release Window: February 23 - March 29, 2026")
    print("="*80)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database()
    
    try:
        # Debug: List all users
        await list_all_users(db)
        
        # Get existing producers
        producer_map, producer_details = await get_existing_producers(db)
        
        if not producer_map:
            print("\n" + "="*80)
            print("ERROR: No existing producers found!")
            print("="*80)
            print("Please create producer accounts first with these names:")
            for name in PRODUCERS:
                print(f"  - {name}")
            print("\nOr update the PRODUCERS list in the script to match existing accounts.")
            return
        
        # Clean up any duplicate movies from previous runs
        await clean_duplicate_movies(db, producer_map)
        
        # Create movies
        movies_created = await create_movies(db, producer_map)
        
        # Save info
        if producer_details:
            save_producer_info(producer_details)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ Existing producers found: {len(producer_map)}")
        print(f"✓ Movies created: {movies_created}")
        print(f"✓ Release window: Feb 23 - March 29, 2026 ({(RELEASE_END - RELEASE_START).days} days)")
        print(f"✓ Info file: backend/scripts/existing_producers_info.txt")
        print("\nProducers with new movies:")
        for name in producer_map.keys():
            print(f"  ✓ {name}")
        print("\nNext Steps:")
        print("  1. Login as any of the above producers")
        print("  2. Go to 'My Movies' to see your new projects")
        print("  3. All movies are set to release in Feb-March 2026")
        print("  4. Use Release Strategy to analyze competition")
        print("="*80)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
