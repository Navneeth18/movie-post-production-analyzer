"""Test the historical movies API endpoint"""
import requests
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_historical_movies(email, password="123456"):
    print(f"Testing Historical Movies API for: {email}")
    print("=" * 70)
    
    # Step 1: Login
    print("\n1. Logging in...")
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            print(response.text)
            return
        
        data = response.json()
        token = data["access_token"]
        
        print(f"✓ Login successful!")
        print(f"  Token: {token[:50]}...")
        
        # Get user info
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        
        if response.status_code == 200:
            user = response.json()
            print(f"  Producer: {user['full_name']}")
            print(f"  Email: {user['email']}")
            print(f"  User ID: {user['id']}")
        else:
            print(f"⚠ Could not fetch user info: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Login error: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 2: Get historical movies
    print(f"\n2. Fetching historical movies...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/movies/historical", headers=headers)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            movies = response.json()
            print(f"✓ Found {len(movies)} historical movies")
            
            if len(movies) > 0:
                print(f"\nMovies:")
                for i, movie in enumerate(movies, 1):
                    print(f"\n{i}. {movie.get('movie_name', 'N/A')}")
                    print(f"   Director: {movie.get('director', 'N/A')}")
                    print(f"   Genre: {movie.get('genre', 'N/A')}")
                    print(f"   Release: {movie.get('release_date', 'N/A')}")
                    print(f"   Budget: ₹{movie.get('budget', 0):,}")
                    print(f"   Revenue: ₹{movie.get('revenue', 0):,}")
                    print(f"   IMDB: {movie.get('imdb_rating', 0)}")
                    print(f"   Tag: {movie.get('tag', 'N/A')}")
            else:
                print("⚠ No historical movies found")
        else:
            print(f"❌ Failed to fetch movies: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error fetching movies: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "prasaddevineni@gmail.com"
    test_historical_movies(email)
