"""Check if artists collection has data"""
import asyncio
from app.db.mongodb import connect_to_mongo, close_mongo_connection, get_database

async def check_artists():
    await connect_to_mongo()
    db = get_database()
    
    print("Checking artists collection...")
    print("=" * 70)
    
    # Count total artists
    total = await db.artists.count_documents({})
    print(f"\nTotal artists in database: {total}")
    
    if total == 0:
        print("\n⚠️  No artists found! Run: python scripts/ingest_csv.py")
        await close_mongo_connection()
        return
    
    # Count by role
    print("\nArtists by Role:")
    for role in ["Director", "Lead 1 (Hero)", "Lead 2 (Heroine)", "Producer"]:
        count = await db.artists.count_documents({"Role": role})
        print(f"  {role}: {count}")
    
    # Count by grade
    print("\nArtists by Grade:")
    for grade in ["Grade 1", "Grade 2", "Grade 3"]:
        count = await db.artists.count_documents({"Grade": grade})
        print(f"  {grade}: {count}")
    
    # Sample artists
    print("\nSample Grade 1 Directors:")
    directors = await db.artists.find({"Role": "Director", "Grade": "Grade 1"}).limit(5).to_list(5)
    for d in directors:
        print(f"  - {d['Name']}")
    
    print("\nSample Grade 1 Heroes:")
    heroes = await db.artists.find({"Role": "Lead 1 (Hero)", "Grade": "Grade 1"}).limit(5).to_list(5)
    for h in heroes:
        print(f"  - {h['Name']}")
    
    print("\n" + "=" * 70)
    print("✅ Artists collection check complete!")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(check_artists())
