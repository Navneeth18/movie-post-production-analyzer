"""Test the combined movies endpoint"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_combined_movies(email, password="123456"):
    print(f"Testing Combined Movies API for: {email}")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": email,
        "password": password
    })
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get user info
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    user = response.json()
    print(f"✓ Logged in as: {user['full_name']}")
    
    # Get all movies (current + historical)
    print(f"\n2. Fetching all movies (current + historical)...")
    response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✓ Found {len(movies)} total movies")
        
        # Separate by source
        current = [m for m in movies if m.get('source') == 'current']
        historical = [m for m in movies if m.get('source') == 'historical']
        
        print(f"  - Current projects: {len(current)}")
        print(f"  - Historical movies: {len(historical)}")
        
        if len(historical) > 0:
            print(f"\nHistorical Movies:")
            for i, movie in enumerate(historical[:5], 1):
                print(f"\n{i}. {movie.get('title', 'N/A')}")
                print(f"   Director: {movie.get('director', 'N/A')}")
                print(f"   Genre: {movie.get('genre', 'N/A')}")
                print(f"   Release: {movie.get('release_date', 'N/A')}")
                print(f"   Budget: ₹{movie.get('budget', 0):,}")
                if movie.get('revenue'):
                    print(f"   Revenue: ₹{movie.get('revenue', 0):,}")
                if movie.get('imdb_rating'):
                    print(f"   IMDB: {movie.get('imdb_rating')}")
                print(f"   Tag: {movie.get('tag')}")
                print(f"   Source: {movie.get('source')}")
        
        if len(current) > 0:
            print(f"\nCurrent Projects:")
            for i, movie in enumerate(current, 1):
                print(f"\n{i}. {movie.get('title', 'N/A')}")
                print(f"   Status: {movie.get('status', 'N/A')}")
                print(f"   Tag: {movie.get('tag')}")
                print(f"   Source: {movie.get('source')}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)
    
    # Test with include_historical=false
    print(f"\n3. Fetching only current movies...")
    response = requests.get(f"{BASE_URL}/movies/?include_historical=false", headers=headers)
    
    if response.status_code == 200:
        movies = response.json()
        print(f"✓ Found {len(movies)} current movies")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    import sys
    email = sys.argv[1] if len(sys.argv) > 1 else "dilraju@gmail.com"
    test_combined_movies(email)
