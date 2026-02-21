"""
Seed Current Movies Script - Version 2
Uses existing talent from bob-dataset.csv and bhanu_dataset.csv
Creates realistic current movie projects with release dates in Feb 23 - March 29, 2026
Shows competitive environment with multiple releases in same period
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from datetime import datetime, timedelta
import random
import pandas as pd
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
import re

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/film_db')

# Release date range: Feb 23, 2026 to March 29, 2026
RELEASE_START = datetime(2026, 2, 23)
RELEASE_END = datetime(2026, 3, 29)

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

def create_email(name):
    """Create email from name - simple format without dots"""
    # Remove special characters and convert to lowercase
    clean_name = re.sub(r'[^a-zA-Z\s]', '', name).lower()
    # Take first and last name
    parts = clean_name.split()
    if len(parts) >= 2:
        email = f"{parts[0]}{parts[-1]}@filmproductions.com"
    else:
        email = f"{parts[0]}@filmproductions.com"
    return email

def load_talent_data():
    """Load talent data from CSV files"""
    print("\n" + "="*80)
    print("Loading Talent Data from CSV Files")
    print("="*80)
    
    # Load bob dataset (producers and directors with grades)
    bob_df = pd.read_csv(Path(__file__).parent.parent / "data" / "bob-dataset.csv")
    
    # Load bhanu dataset (for heroes and heroines)
    bhanu_df = pd.read_csv(Path(__file__).parent.parent / "data" / "bhanu_dataset.csv")
    
    # Get producers by grade
    producers = bob_df[bob_df['Role'] == 'Producer'].copy()
    producers_by_grade = {
        'Grade 1': producers[producers['Grade'] == 'Grade 1']['Name'].tolist(),
        'Grade 2': producers[producers['Grade'] == 'Grade 2']['Name'].tolist(),
        'Grade 3': producers[producers['Grade'] == 'Grade 3']['Name'].tolist()
    }
    
    # Get directors by grade
    directors = bob_df[bob_df['Role'] == 'Director'].copy()
    directors_by_grade = {
        'Grade 1': directors[directors['Grade'] == 'Grade 1']['Name'].tolist(),
        'Grade 2': directors[directors['Grade'] == 'Grade 2']['Name'].tolist(),
        'Grade 3': directors[directors['Grade'] == 'Grade 3']['Name'].tolist()
    }
    
    # Get unique heroes and heroines from bhanu dataset
    heroes = bhanu_df['hero'].dropna().unique().tolist()
    heroines = bhanu_df['heroine'].dropna().unique().tolist()
    
    print(f"✓ Loaded {len(producers)} producers")
    print(f"  Grade 1: {len(producers_by_grade['Grade 1'])}")
    print(f"  Grade 2: {len(producers_by_grade['Grade 2'])}")
    print(f"  Grade 3: {len(producers_by_grade['Grade 3'])}")
    print(f"✓ Loaded {len(directors)} directors")
    print(f"  Grade 1: {len(directors_by_grade['Grade 1'])}")
    print(f"  Grade 2: {len(directors_by_grade['Grade 2'])}")
    print(f"  Grade 3: {len(directors_by_grade['Grade 3'])}")
    print(f"✓ Loaded {len(heroes)} unique heroes")
    print(f"✓ Loaded {len(heroines)} unique heroines")
    
    return producers_by_grade, directors_by_grade, heroes, heroines

def select_producers(producers_by_grade, count=12):
    """Select diverse set of producers"""
    selected = []
    
    # Select 2 Grade 1 (big)
    if producers_by_grade['Grade 1']:
        selected.extend(random.sample(producers_by_grade['Grade 1'], min(2, len(producers_by_grade['Grade 1']))))
    
    # Select 4 Grade 2 (medium)
    if producers_by_grade['Grade 2']:
        selected.extend(random.sample(producers_by_grade['Grade 2'], min(4, len(producers_by_grade['Grade 2']))))
    
    # Select 6 Grade 3 (small)
    if producers_by_grade['Grade 3']:
        selected.extend(random.sample(producers_by_grade['Grade 3'], min(6, len(producers_by_grade['Grade 3']))))
    
    return selected[:count]

def generate_release_dates(count):
    """Generate release dates between Feb 23 and March 29, 2026"""
    # Calculate total days in range
    total_days = (RELEASE_END - RELEASE_START).days
    
    # Generate random dates
    dates = []
    for _ in range(count):
        random_days = random.randint(0, total_days)
        release_date = RELEASE_START + timedelta(days=random_days)
        dates.append(release_date)
    
    # Sort dates to show chronological order
    dates.sort()
    return dates

def generate_movie_combinations(producers_by_grade, directors_by_grade, heroes, heroines, count=16):
    """Generate diverse movie combinations covering all grade scenarios"""
    combinations = []
    
    # Define combination templates (producer_grade, director_grade, budget_range)
    templates = [
        # Big productions
        ('Grade 1', 'Grade 1', (150000000, 250000000)),  # 2 movies
        ('Grade 1', 'Grade 1', (150000000, 250000000)),
        ('Grade 1', 'Grade 2', (100000000, 150000000)),  # 1 movie
        
        # Medium productions
        ('Grade 2', 'Grade 1', (80000000, 120000000)),   # 2 movies
        ('Grade 2', 'Grade 1', (80000000, 120000000)),
        ('Grade 2', 'Grade 2', (50000000, 80000000)),    # 4 movies
        ('Grade 2', 'Grade 2', (50000000, 80000000)),
        ('Grade 2', 'Grade 2', (50000000, 80000000)),
        ('Grade 2', 'Grade 2', (50000000, 80000000)),
        
        # Small productions
        ('Grade 3', 'Grade 2', (25000000, 40000000)),    # 3 movies
        ('Grade 3', 'Grade 2', (25000000, 40000000)),
        ('Grade 3', 'Grade 2', (25000000, 40000000)),
        ('Grade 3', 'Grade 3', (10000000, 25000000)),    # 4 movies
        ('Grade 3', 'Grade 3', (10000000, 25000000)),
        ('Grade 3', 'Grade 3', (10000000, 25000000)),
        ('Grade 3', 'Grade 3', (10000000, 25000000)),
    ]
    
    # Generate release dates for competitive environment
    release_dates = generate_release_dates(count)
    
    for idx, (prod_grade, dir_grade, budget_range) in enumerate(templates[:count]):
        # Select producer
        if producers_by_grade[prod_grade]:
            producer = random.choice(producers_by_grade[prod_grade])
        else:
            producer = random.choice(producers_by_grade['Grade 3'])
        
        # Select director
        if directors_by_grade[dir_grade]:
            director = random.choice(directors_by_grade[dir_grade])
        else:
            director = random.choice(directors_by_grade['Grade 3'])
        
        # Select hero and heroine
        hero = random.choice(heroes)
        heroine = random.choice(heroines)
        
        # Generate movie details
        title_base = random.choice(MOVIE_TITLES)
        title_suffix = random.choice(["", " Returns", " 2.0", " Reborn", " Rising", ""])
        title = f"{title_base}{title_suffix}"
        
        budget = random.randint(budget_range[0], budget_range[1])
        genres = random.choice(GENRES_LIST)
        languages = random.choice(LANGUAGES_LIST)
        region = random.choice(REGIONS)
        status = random.choice(STATUSES)
        
        combinations.append({
            'title': title,
            'producer': producer,
            'producer_grade': prod_grade,
            'director': director,
            'director_grade': dir_grade,
            'hero': hero,
            'heroine': heroine,
            'genres': genres,
            'languages': languages,
            'region': region,
            'budget': budget,
            'status': status,
            'release_date': release_dates[idx]
        })
    
    return combinations

async def create_producer_accounts(db, selected_producers, producers_by_grade):
    """Create producer user accounts"""
    print("\n" + "="*80)
    print("Creating Producer Accounts")
    print("="*80)
    
    producer_ids = {}
    producer_details = []
    
    for producer_name in selected_producers:
        # Determine grade
        grade = None
        for g, names in producers_by_grade.items():
            if producer_name in names:
                grade = g
                break
        
        # Create email
        email = create_email(producer_name)
        username = email.split('@')[0]
        password = "Producer@123"
        
        # Check if already exists
        existing = await db.users.find_one({"email": email})
        
        if existing:
            print(f"✓ Producer already exists: {producer_name}")
            producer_ids[producer_name] = str(existing['_id'])
            producer_details.append({
                'name': producer_name,
                'email': email,
                'username': username,
                'password': password,
                'grade': grade
            })
            continue
        
        # Create new producer
        user_doc = {
            "username": username,
            "email": email,
            "hashed_password": pwd_context.hash(password),
            "role": "producer",
            "full_name": producer_name,
            "company": f"{producer_name} Productions",
            "tier": "big" if grade == "Grade 1" else "medium" if grade == "Grade 2" else "small",
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_doc)
        producer_ids[producer_name] = str(result.inserted_id)
        
        producer_details.append({
            'name': producer_name,
            'email': email,
            'username': username,
            'password': password,
            'grade': grade
        })
        
        print(f"✓ Created: {producer_name} ({email}) - {grade}")
    
    return producer_ids, producer_details

async def create_movies(db, combinations, producer_ids):
    """Create current movie projects"""
    print("\n" + "="*80)
    print("Creating Current Movie Projects")
    print("Release Window: Feb 23, 2026 - March 29, 2026")
    print("="*80)
    
    movies_created = 0
    
    for combo in combinations:
        producer_id = producer_ids.get(combo['producer'])
        
        if not producer_id:
            print(f"  ⊘ Skipping {combo['title']} - Producer not found")
            continue
        
        # Check if movie already exists
        existing = await db.movies.find_one({
            "title": combo['title'],
            "producer_id": producer_id
        })
        
        if existing:
            print(f"  ⊘ Movie already exists: {combo['title']}")
            continue
        
        # Create movie document
        movie_doc = {
            "title": combo['title'],
            "director": combo['director'],
            "genres": combo['genres'],
            "budget": combo['budget'],
            "budget_currency": "INR",
            "release_date": combo['release_date'],
            "languages": combo['languages'],
            "region": combo['region'],
            "cast": [
                {
                    "name": combo['hero'],
                    "role": "Lead 1 (Hero)",
                    "star_power": None
                },
                {
                    "name": combo['heroine'],
                    "role": "Lead 2 (Heroine)",
                    "star_power": None
                }
            ],
            "producer_id": producer_id,
            "status": combo['status'],
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
        
        budget_cr = combo['budget'] / 10000000
        release_str = combo['release_date'].strftime('%b %d, %Y')
        print(f"  ✓ {combo['title']}")
        print(f"    Release: {release_str}")
        print(f"    Producer: {combo['producer']} ({combo['producer_grade']})")
        print(f"    Director: {combo['director']} ({combo['director_grade']})")
        print(f"    Cast: {combo['hero']} & {combo['heroine']}")
        print(f"    Budget: ₹{budget_cr:.1f}Cr | Status: {combo['status']}")
        print()
    
    return movies_created

def save_producer_credentials(producer_details):
    """Save producer credentials to text file"""
    print("\n" + "="*80)
    print("Saving Producer Credentials")
    print("="*80)
    
    credentials_file = Path(__file__).parent / "producer_credentials.txt"
    
    with open(credentials_file, 'w') as f:
        f.write("="*80 + "\n")
        f.write("PRODUCER CREDENTIALS\n")
        f.write("Film Intel Platform - Current Movie Projects\n")
        f.write("Competitive Release Window: Feb 23 - March 29, 2026\n")
        f.write("="*80 + "\n\n")
        
        f.write("LOGIN URL: http://localhost:5173/login\n")
        f.write("DEFAULT PASSWORD: Producer@123\n\n")
        
        # Sort by grade
        for grade in ['Grade 1', 'Grade 2', 'Grade 3']:
            grade_producers = [p for p in producer_details if p['grade'] == grade]
            if grade_producers:
                f.write(f"\n{grade} PRODUCERS ({len(grade_producers)}):\n")
                f.write("-" * 80 + "\n")
                for i, prod in enumerate(grade_producers, 1):
                    f.write(f"{i}. {prod['name']}\n")
                    f.write(f"   Email: {prod['email']}\n")
                    f.write(f"   Username: {prod['username']}\n")
                    f.write(f"   Password: {prod['password']}\n\n")
        
        f.write("="*80 + "\n")
        f.write("NOTES:\n")
        f.write("- All producers use the same password: Producer@123\n")
        f.write("- All movies release between Feb 23 - March 29, 2026\n")
        f.write("- This creates a competitive environment with multiple releases\n")
        f.write("- Grade 1 producers have high-budget projects (₹15Cr+)\n")
        f.write("- Grade 2 producers have mid-budget projects (₹5-15Cr)\n")
        f.write("- Grade 3 producers have low-budget projects (<₹5Cr)\n")
        f.write("- Talent data sourced from bob-dataset.csv and bhanu_dataset.csv\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Credentials saved to: {credentials_file}")

async def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("SEED CURRENT MOVIES - COMPETITIVE ENVIRONMENT")
    print("Release Window: February 23 - March 29, 2026")
    print("="*80)
    
    # Load talent data
    producers_by_grade, directors_by_grade, heroes, heroines = load_talent_data()
    
    # Select producers
    selected_producers = select_producers(producers_by_grade, count=12)
    print(f"\n✓ Selected {len(selected_producers)} producers for accounts")
    
    # Generate movie combinations
    combinations = generate_movie_combinations(
        producers_by_grade, directors_by_grade, heroes, heroines, count=16
    )
    print(f"✓ Generated {len(combinations)} movie combinations")
    print(f"✓ Release dates spread across {(RELEASE_END - RELEASE_START).days} days")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGO_URI)
    db = client.get_database()
    
    try:
        # Create producer accounts
        producer_ids, producer_details = await create_producer_accounts(
            db, selected_producers, producers_by_grade
        )
        
        # Create movies
        movies_created = await create_movies(db, combinations, producer_ids)
        
        # Save credentials
        save_producer_credentials(producer_details)
        
        # Summary
        print("\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        print(f"✓ Producers created/verified: {len(producer_ids)}")
        print(f"✓ Movies created: {movies_created}")
        print(f"✓ Release window: Feb 23 - March 29, 2026 ({(RELEASE_END - RELEASE_START).days} days)")
        print(f"✓ Credentials file: backend/scripts/producer_credentials.txt")
        print("\nCompetitive Environment:")
        print("  ✓ Multiple movies releasing in same period")
        print("  ✓ Mix of big, medium, and small budget films")
        print("  ✓ Various genres competing for audience")
        print("\nGrade Coverage:")
        print("  ✓ Grade 1 Producer + Grade 1 Director (Big Budget)")
        print("  ✓ Grade 1 Producer + Grade 2 Director")
        print("  ✓ Grade 2 Producer + Grade 1 Director")
        print("  ✓ Grade 2 Producer + Grade 2 Director (Medium Budget)")
        print("  ✓ Grade 3 Producer + Grade 2 Director")
        print("  ✓ Grade 3 Producer + Grade 3 Director (Small Budget)")
        print("\nData Source:")
        print("  ✓ Producers & Directors: bob-dataset.csv")
        print("  ✓ Heroes & Heroines: bhanu_dataset.csv")
        print("="*80)
        
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())
