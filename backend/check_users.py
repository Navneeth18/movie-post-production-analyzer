"""Check if users were created"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "film_intel_db"

async def check_users():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    try:
        total_users = await db.users.count_documents({})
        migrated_users = await db.users.count_documents({"is_migrated": True})
        
        print(f"Total users: {total_users}")
        print(f"Migrated producers: {migrated_users}")
        
        if migrated_users > 0:
            sample = await db.users.find_one({"is_migrated": True})
            print(f"\nSample producer:")
            print(f"  Name: {sample.get('full_name')}")
            print(f"  Email: {sample.get('email')}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(check_users())
