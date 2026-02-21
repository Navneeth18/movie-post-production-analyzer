"""Test historical movies API"""
import requests

BASE_URL = "http://localhost:8000/api"

# Test with a producer account
# Using Prasad Devineni (producer of Bāhubali)
email = "prasaddevineni@gmail.com"
password = "123456"

print("Testing Historical Movies API")
print("=" * 60)

# Login
print(f"\n1. Logging in as {email}...")
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": email,
    "password": password
})

if response.status_code == 200:
    data = response.json()
    token = data["access_token"]
    print(f"✓ Login successful!")
    print(f"  Producer: {data['user']['full_name']}")
    
    # Get historical movies
    print(f"\n2. Fetching historical movies...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/movies/historical", headers=headers)
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✓ Found {len(movies)} historical movies")
        
        if len(movies) > 0:
            print(f"\nSample movies:")
            for movie in movies[:5]:
                print(f"  - {movie['movie_name']} ({movie.get('release_date', 'N/A')})")
                print(f"    Budget: ₹{movie.get('budget', 0):,} | Revenue: ₹{movie.get('revenue', 0):,}")
                print(f"    IMDB: {movie.get('imdb_rating', 0)} | Genre: {movie.get('genre', 'N/A')}")
                print()
    else:
        print(f"❌ Failed to fetch movies: {response.status_code}")
        print(response.text)
else:
    print(f"❌ Login failed: {response.status_code}")
    print(response.text)

print("=" * 60)
