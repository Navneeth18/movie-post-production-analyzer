"""Test /movies/all endpoint"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_all_movies():
    print("Testing /movies/all Endpoint")
    print("=" * 70)
    
    # Login
    print("\n1. Login...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "dilraju@gmail.com",
        "password": "123456"
    })
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.text}")
        return
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")
    
    # Test /movies/all with tag=current
    print("\n2. Testing /movies/all?tag=current...")
    response = requests.get(f"{BASE_URL}/movies/all?tag=current", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        movies = response.json()
        print(f"Found {len(movies)} current movies")
        
        if movies:
            print("\nSample movie:")
            movie = movies[0]
            print(f"  Title: {movie.get('title')}")
            print(f"  Director: {movie.get('director')}")
            print(f"  Status: {movie.get('status')}")
            print(f"  Tag: {movie.get('tag')}")
            print(f"  HWS Score: {movie.get('hws_score')}")
            print(f"  Category: {movie.get('category')}")
    else:
        print(f"Failed: {response.text}")
    
    # Test /movies/all with tag=past
    print("\n3. Testing /movies/all?tag=past...")
    response = requests.get(f"{BASE_URL}/movies/all?tag=past", headers=headers)
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        movies = response.json()
        print(f"Found {len(movies)} past movies")
    else:
        print(f"Failed: {response.text}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_all_movies()
