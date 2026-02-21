"""Test HWS calculation through API"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_hws_api():
    print("Testing HWS Calculation through API")
    print("=" * 70)
    
    # Login as a producer
    print("\n1. Login as producer...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "dilraju@gmail.com",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✅ Login successful")
    
    # Get movies
    print("\n2. Fetching movies...")
    movies_response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    
    if movies_response.status_code != 200:
        print(f"❌ Failed to fetch movies: {movies_response.text}")
        return
    
    movies = movies_response.json()
    print(f"✅ Found {len(movies)} movies")
    
    # Display first 3 movies with HWS scores
    print("\n3. Movie HWS Scores:")
    print("-" * 70)
    for movie in movies[:3]:
        print(f"\nTitle: {movie.get('title')}")
        print(f"Director: {movie.get('director')}")
        print(f"Cast Score: {movie.get('cast_score', 'N/A')}")
        print(f"HWS Score: {movie.get('hws_score', 'N/A')}")
        print(f"Category: {movie.get('category', 'N/A')}")
        print(f"Source: {movie.get('source', 'N/A')}")
        
        if movie.get('hws_breakdown'):
            print("\nHWS Breakdown:")
            breakdown = movie['hws_breakdown']
            print(f"  Director: {breakdown.get('director_contribution', 'N/A')}")
            print(f"  Hero: {breakdown.get('hero_contribution', 'N/A')}")
            print(f"  Heroine: {breakdown.get('heroine_contribution', 'N/A')}")
            print(f"  Genre: {breakdown.get('genre_contribution', 'N/A')}")
            print(f"  Popularity: {breakdown.get('popularity_contribution', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("✅ API HWS Test Complete!")

if __name__ == "__main__":
    test_hws_api()
