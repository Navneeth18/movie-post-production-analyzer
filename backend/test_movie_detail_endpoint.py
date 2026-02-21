"""Test movie detail endpoint"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_movie_detail():
    print("Testing Movie Detail Endpoint")
    print("=" * 70)
    
    # Login
    print("\n1. Login...")
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
    
    # Get movies list
    print("\n2. Getting movies list...")
    movies_response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    
    if movies_response.status_code != 200:
        print(f"❌ Failed to get movies: {movies_response.text}")
        return
    
    movies = movies_response.json()
    if not movies:
        print("❌ No movies found")
        return
    
    print(f"✅ Found {len(movies)} movies")
    
    # Get first movie ID
    movie_id = movies[0]["id"]
    print(f"\n3. Testing movie detail for ID: {movie_id}")
    
    # Test movie detail endpoint
    detail_response = requests.get(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    
    print(f"Status Code: {detail_response.status_code}")
    
    if detail_response.status_code == 200:
        movie = detail_response.json()
        print("✅ Movie detail retrieved successfully!")
        print(f"\nMovie Details:")
        print(f"  Title: {movie.get('title')}")
        print(f"  Director: {movie.get('director')}")
        print(f"  Cast Score: {movie.get('cast_score')}")
        print(f"  HWS Score: {movie.get('hws_score')}")
        print(f"  Category: {movie.get('category')}")
        
        if movie.get('hws_breakdown'):
            print(f"\n  HWS Breakdown:")
            breakdown = movie['hws_breakdown']
            print(f"    Director: {breakdown.get('director_contribution')}")
            print(f"    Hero: {breakdown.get('hero_contribution')}")
            print(f"    Genre: {breakdown.get('genre_contribution')}")
    else:
        print(f"❌ Failed to get movie detail")
        print(f"Response: {detail_response.text}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_movie_detail()
