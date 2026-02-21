"""Check Test Movie for Public Pulse details"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/film_db')

async def check_test_movie():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database()
    
    try:
        # Find user with dilraju@filmproductions.com
        user = await db.users.find_one({'email': 'dilraju@filmproductions.com'})
        
        if not user:
            print("User dilraju@filmproductions.com not found!")
            return
        
        print(f"User: {user.get('full_name', 'N/A')}")
        print(f"Email: {user.get('email')}")
        print(f"ID: {str(user['_id'])}")
        
        # Find all movies for this user
        movies = await db.movies.find({'producer_id': str(user['_id'])}).to_list(100)
        
        print(f"\nTotal movies: {len(movies)}")
        print("\nMovies:")
        for m in movies:
            print(f"\n  Title: {m['title']}")
            print(f"  Release Date: {m.get('release_date', 'No date')}")
            print(f"  Status: {m.get('status', 'N/A')}")
            print(f"  Tag: {m.get('tag', 'N/A')}")
            print(f"  Genre: {m.get('genre', m.get('genres', 'N/A'))}")
            print(f"  Budget: {m.get('budget', 0)}")
            print(f"  ID: {str(m['_id'])}")
        
        # Find Test Movie specifically
        test_movie = await db.movies.find_one({
            'producer_id': str(user['_id']),
            'title': 'Test Movie for Public Pulse'
        })
        
        if test_movie:
            print("\n" + "="*80)
            print("TEST MOVIE FOR PUBLIC PULSE - DETAILS")
            print("="*80)
            print(f"Title: {test_movie['title']}")
            print(f"Release Date: {test_movie.get('release_date', 'No date')}")
            print(f"Status: {test_movie.get('status', 'N/A')}")
            print(f"Tag: {test_movie.get('tag', 'N/A')}")
            print(f"Genre: {test_movie.get('genre', test_movie.get('genres', 'N/A'))}")
            print(f"Budget: {test_movie.get('budget', 0)}")
            print(f"Director: {test_movie.get('director', 'N/A')}")
            print(f"ID: {str(test_movie['_id'])}")
            
            # Check for competitors
            if test_movie.get('release_date'):
                from datetime import timedelta
                release_date = test_movie['release_date']
                start_date = release_date - timedelta(days=30)
                end_date = release_date + timedelta(days=30)
                
                competitors = await db.movies.find({
                    '_id': {'$ne': test_movie['_id']},
                    'release_date': {
                        '$gte': start_date,
                        '$lte': end_date
                    }
                }).to_list(100)
                
                print(f"\nCompetitors in ±30 days window:")
                print(f"Total: {len(competitors)}")
                for comp in competitors:
                    days_diff = abs((comp['release_date'] - release_date).days)
                    print(f"  - {comp['title']}: {comp.get('release_date')} ({days_diff} days away)")
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_test_movie())
