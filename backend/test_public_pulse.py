"""Test public pulse endpoints"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_public_pulse():
    print("Testing Public Pulse Endpoints")
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
    
    # Get movies
    print("\n2. Getting movies...")
    movies_response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    
    if movies_response.status_code != 200:
        print(f"Failed to get movies: {movies_response.text}")
        return
    
    movies = movies_response.json()
    print(f"Found {len(movies)} movies")
    
    # Find a current movie (not historical)
    current_movie = None
    for movie in movies:
        if movie.get("source") == "current" or movie.get("tag") == "current":
            current_movie = movie
            break
    
    if not current_movie:
        print("No current movies found, creating one...")
        
        # Create a test movie
        create_response = requests.post(
            f"{BASE_URL}/movies/",
            headers=headers,
            json={
                "title": "Test Movie for Public Pulse",
                "director": "S. S. Rajamouli",
                "genres": ["Action", "Drama"],
                "languages": ["Telugu", "Hindi"],
                "budget": 200000000,
                "region": "India",
                "status": "production",
                "cast": [
                    {"name": "Prabhas", "role": "Hero"},
                    {"name": "Anushka Shetty", "role": "Heroine"}
                ]
            }
        )
        
        if create_response.status_code != 201:
            print(f"Failed to create movie: {create_response.text}")
            return
        
        current_movie = create_response.json()
        print(f"Created movie: {current_movie['title']}")
    
    movie_id = current_movie["id"]
    print(f"Using movie: {current_movie['title']} (ID: {movie_id})")
    
    # Test add trailer endpoint
    print("\n3. Testing add-trailer endpoint...")
    trailer_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    response = requests.post(
        f"{BASE_URL}/public-pulse/{movie_id}/add-trailer",
        headers=headers,
        json={"youtube_url": trailer_url}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Trailer added successfully!")
        data = response.json()
        print(f"Video ID: {data.get('video_id')}")
        print(f"Pulse Score: {data.get('pulse_score')}")
    else:
        print(f"Failed: {response.text}")
    
    # Test get current pulse
    print("\n4. Testing get current pulse...")
    response = requests.get(
        f"{BASE_URL}/public-pulse/{movie_id}/current",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Current pulse retrieved!")
        data = response.json()
        print(f"Pulse Score: {data.get('current_pulse_score')}")
        print(f"Sentiment: {data.get('sentiment')}")
    else:
        print(f"Response: {response.text}")
    
    # Test get history
    print("\n5. Testing get pulse history...")
    response = requests.get(
        f"{BASE_URL}/public-pulse/{movie_id}/history",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        history = response.json()
        print(f"Found {len(history)} history records")
    else:
        print(f"Response: {response.text}")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_public_pulse()
