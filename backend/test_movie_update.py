"""Test movie update endpoint"""
import requests

BASE_URL = "http://localhost:8000/api/v1"

def test_movie_update():
    print("Testing Movie Update Endpoint")
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
    movies = movies_response.json()
    
    # Find a current movie
    current_movie = None
    for movie in movies:
        if movie.get("tag") == "current" or movie.get("source") == "current":
            current_movie = movie
            break
    
    if not current_movie:
        print("No current movies found, creating one...")
        create_response = requests.post(
            f"{BASE_URL}/movies/",
            headers=headers,
            json={
                "title": "Test Update Movie",
                "director": "S. S. Rajamouli",
                "genres": ["Action"],
                "languages": ["Telugu"],
                "budget": 100000000,
                "region": "India",
                "status": "production",
                "cast": [{"name": "Prabhas", "role": "Hero"}]
            }
        )
        current_movie = create_response.json()
    
    movie_id = current_movie["id"]
    print(f"Using movie: {current_movie['title']} (ID: {movie_id})")
    print(f"Current status: {current_movie.get('status')}")
    print(f"Current genres: {current_movie.get('genres')}")
    
    # Update movie
    print("\n3. Updating movie...")
    update_data = {
        "status": "post-production",
        "genres": ["Action", "Drama", "Thriller"]
    }
    
    update_response = requests.put(
        f"{BASE_URL}/movies/{movie_id}",
        headers=headers,
        json=update_data
    )
    
    print(f"Status: {update_response.status_code}")
    if update_response.status_code == 200:
        updated_movie = update_response.json()
        print("Movie updated successfully!")
        print(f"New status: {updated_movie.get('status')}")
        print(f"New genres: {updated_movie.get('genres')}")
        print(f"HWS Score: {updated_movie.get('hws_score')}")
        print(f"Category: {updated_movie.get('category')}")
    else:
        print(f"Failed: {update_response.text}")
    
    # Verify update persisted
    print("\n4. Verifying update...")
    get_response = requests.get(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    
    if get_response.status_code == 200:
        movie = get_response.json()
        print(f"Verified status: {movie.get('status')}")
        print(f"Verified genres: {movie.get('genres')}")
        
        if movie.get('status') == update_data['status']:
            print("Status update verified!")
        else:
            print("ERROR: Status not updated!")
        
        if movie.get('genres') == update_data['genres']:
            print("Genres update verified!")
        else:
            print("ERROR: Genres not updated!")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    test_movie_update()
