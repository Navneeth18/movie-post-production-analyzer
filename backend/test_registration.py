import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from app.services.auth_service import get_password_hash

async def test_registration():
    try:
        # Test MongoDB connection
        client = AsyncIOMotorClient("mongodb://localhost:27017")
        db = client["film_intel_db"]
        
        # Test password hashing
        password = "test123"
        hashed = get_password_hash(password)
        print(f"✓ Password hashing works: {hashed[:20]}...")
        
        # Test database connection
        await db.command("ping")
        print("✓ MongoDB connection successful")
        
        # Test user creation
        test_user = {
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "hashed_password": hashed,
            "is_active": True
        }
        
        # Check if user exists
        existing = await db.users.find_one({"email": test_user["email"]})
        if existing:
            print("✓ Test user already exists")
            await db.users.delete_one({"email": test_user["email"]})
            print("✓ Cleaned up test user")
        
        # Insert test user
        result = await db.users.insert_one(test_user)
        print(f"✓ User created with ID: {result.inserted_id}")
        
        # Verify user was created
        user = await db.users.find_one({"_id": result.inserted_id})
        if user:
            print(f"✓ User verified: {user['username']}")
        
        # Cleanup
        await db.users.delete_one({"_id": result.inserted_id})
        print("✓ Test user cleaned up")
        
        print("\n✅ All tests passed! Registration should work.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure MongoDB is running:")
        print("  - Windows: Start MongoDB service")
        print("  - Mac/Linux: mongod")
        sys.exit(1)
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_registration())
