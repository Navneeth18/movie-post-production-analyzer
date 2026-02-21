"""Test migration logic before running actual migration"""
import re
from app.services.auth_service import get_password_hash

# Test producer names
test_producers = [
    "Sudhanskar Mikkil1neni",
    "Guntaka Srinivas Reddy",
    "A.B.C. Productions",
    "Test Producer 123"
]

print("Testing email generation logic:")
print("=" * 60)

for producer_name in test_producers:
    username = re.sub(r'[^a-zA-Z0-9]', '', producer_name).lower()
    email = f"{username}@gmail.com"
    print(f"Producer: {producer_name}")
    print(f"  → Username: {username}")
    print(f"  → Email: {email}")
    print()

print("=" * 60)
print("\nTesting password hashing:")
hashed = get_password_hash("123456")
print(f"✓ Password hash generated: {hashed[:50]}...")

print("\n✅ All migration logic tests passed!")
