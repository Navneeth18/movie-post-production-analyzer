"""Test that historical movies cannot use public pulse, competitors, and strategy"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_historical_restrictions():
    print("Testing Historical Movie Restrictions")
    print("=" * 70)
    
    # Login
    print("\n1. Login...")
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "dilraju@gmail.com",
        "password": "123456"
    })
    
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login successful")
    
    # Get movies
    print("\n2. Getting movies...")
    movies_response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    movies = movies_response.json()
    
    # Find a historical movie
    historical_movie = None
    for movie in movies:
        if movie.get("tag") == "past" or movie.get("source") == "historical":
            historical_movie = movie
            break
    
    if not historical_movie:
        print("No historical movies found")
        return
    
    movie_id = historical_movie["id"]
    print(f"Using historical movie: {historical_movie['title']} (ID: {movie_id})")
    print(f"Tag: {historical_movie.get('tag')}")
    
    # Test 1: Try to add trailer (should fail)
    print("\n3. Testing add-trailer on historical movie...")
    response = requests.post(
        f"{BASE_URL}/public-pulse/{movie_id}/add-trailer",
        headers=headers,
        json={"youtube_url": "https://www.youtube.com/watch?v=test"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("PASS: Historical movie blocked from public pulse")
        print(f"Message: {response.json().get('detail')}")
    else:
        print("FAIL: Historical movie should not be able to add trailer")
    
    # Test 2: Try to analyze competitor (should fail)
    print("\n4. Testing competitor analysis on historical movie...")
    
    # Find another movie to use as competitor
    competitor_id = None
    for movie in movies:
        if movie["id"] != movie_id:
            competitor_id = movie["id"]
            break
    
    if competitor_id:
        response = requests.post(
            f"{BASE_URL}/movies/{movie_id}/analyze-competitor",
            headers=headers,
            json={"competitor_movie_id": competitor_id}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 400:
            print("PASS: Historical movie blocked from competitor analysis")
            print(f"Message: {response.json().get('detail')}")
        else:
            print("FAIL: Historical movie should not be able to analyze competitors")
    
    # Test 3: Try release strategy (should fail)
    print("\n5. Testing release strategy on historical movie...")
    response = requests.post(
        f"{BASE_URL}/release-strategy/analyze-date-range",
        headers=headers,
        json={"movie_id": movie_id}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 400:
        print("PASS: Historical movie blocked from release strategy")
        print(f"Message: {response.json().get('detail')}")
    else:
        print("FAIL: Historical movie should not be able to use release strategy")
    
    # Test 4: Verify current movie CAN use these features
    print("\n6. Testing current movie CAN use features...")
    current_movie = None
    for movie in movies:
        if movie.get("tag") == "current" or movie.get("source") == "current":
            current_movie = movie
            break
    
    if current_movie:
        movie_id = current_movie["id"]
        print(f"Using current movie: {current_movie['title']}")
        
        response = requests.post(
            f"{BASE_URL}/public-pulse/{movie_id}/add-trailer",
            headers=headers,
            json={"youtube_url": "https://www.youtube.com/watch?v=test"}
        )
        
        if response.status_code in [200, 201]:
            print("PASS: Current movie can use public pulse")
        else:
            print(f"Note: {response.status_code} - {response.json().get('detail')}")
    
    print("\n" + "=" * 70)
    print("Restrictions test complete!")

if __name__ == "__main__":
    test_historical_restrictions()
