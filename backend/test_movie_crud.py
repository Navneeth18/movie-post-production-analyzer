"""Test movie CRUD operations with new schema"""
import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_movie_crud():
    print("Testing Movie CRUD Operations")
    print("=" * 70)
    
    # Login
    print("\n1. Logging in...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "dilraju@gmail.com",
        "password": "123456"
    })
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.status_code}")
        return
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✓ Logged in as Dil Raju")
    
    # Create a new movie
    print("\n2. Creating new movie...")
    new_movie = {
        "title": "Test Movie 2026",
        "director": "Test Director",
        "genres": ["Action", "Drama", "Thriller"],  # Multiple genres
        "languages": ["Telugu", "Hindi", "Tamil"],  # Multiple languages
        "budget": 50000000,
        "budget_currency": "INR",
        "release_date": "2026-12-25T00:00:00",
        "region": "Pan-India",
        "status": "pre-production",
        "cast": [
            {"name": "Actor 1", "role": "Hero", "star_power": 85},
            {"name": "Actor 2", "role": "Heroine", "star_power": 75}
        ]
    }
    
    response = requests.post(f"{BASE_URL}/movies/", json=new_movie, headers=headers)
    
    if response.status_code == 201:
        movie = response.json()
        movie_id = movie["id"]
        print(f"✓ Movie created successfully!")
        print(f"  ID: {movie_id}")
        print(f"  Title: {movie['title']}")
        print(f"  Genres: {', '.join(movie['genres'])}")
        print(f"  Languages: {', '.join(movie['languages'])}")
        print(f"  Status: {movie['status']}")
        print(f"  Cast Score: {movie.get('cast_score', 0)}")
        print(f"  Historic Score: {movie.get('historic_score', 0)}")
    else:
        print(f"❌ Failed to create movie: {response.status_code}")
        print(response.text)
        return
    
    # Get the movie
    print(f"\n3. Fetching movie details...")
    response = requests.get(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✓ Movie fetched successfully!")
        print(f"  Title: {movie['title']}")
        print(f"  Status: {movie['status']}")
    else:
        print(f"❌ Failed to fetch movie: {response.status_code}")
    
    # Update the movie - change status
    print(f"\n4. Updating movie status to 'production'...")
    update_data = {
        "status": "production"
    }
    
    response = requests.put(f"{BASE_URL}/movies/{movie_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✓ Movie updated successfully!")
        print(f"  Status: {movie['status']}")
    else:
        print(f"❌ Failed to update movie: {response.status_code}")
        print(response.text)
    
    # Update release date and status
    print(f"\n5. Updating release date and status to 'awaiting-release'...")
    update_data = {
        "release_date": "2027-01-15T00:00:00",
        "status": "awaiting-release"
    }
    
    response = requests.put(f"{BASE_URL}/movies/{movie_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✓ Movie updated successfully!")
        print(f"  Release Date: {movie['release_date']}")
        print(f"  Status: {movie['status']}")
    else:
        print(f"❌ Failed to update movie: {response.status_code}")
        print(response.text)
    
    # Update genres and languages
    print(f"\n6. Updating genres and languages...")
    update_data = {
        "genres": ["Action", "Thriller"],
        "languages": ["Telugu", "Hindi"]
    }
    
    response = requests.put(f"{BASE_URL}/movies/{movie_id}", json=update_data, headers=headers)
    
    if response.status_code == 200:
        movie = response.json()
        print(f"✓ Movie updated successfully!")
        print(f"  Genres: {', '.join(movie['genres'])}")
        print(f"  Languages: {', '.join(movie['languages'])}")
    else:
        print(f"❌ Failed to update movie: {response.status_code}")
        print(response.text)
    
    # Get all movies
    print(f"\n7. Fetching all movies...")
    response = requests.get(f"{BASE_URL}/movies/", headers=headers)
    
    if response.status_code == 200:
        movies = response.json()
        current = [m for m in movies if m.get('source') == 'current']
        historical = [m for m in movies if m.get('source') == 'historical']
        print(f"✓ Found {len(movies)} total movies")
        print(f"  Current projects: {len(current)}")
        print(f"  Historical movies: {len(historical)}")
    else:
        print(f"❌ Failed to fetch movies: {response.status_code}")
    
    # Delete the test movie
    print(f"\n8. Deleting test movie...")
    response = requests.delete(f"{BASE_URL}/movies/{movie_id}", headers=headers)
    
    if response.status_code == 204:
        print(f"✓ Movie deleted successfully!")
    else:
        print(f"❌ Failed to delete movie: {response.status_code}")
    
    print("\n" + "=" * 70)
    print("✅ All tests completed!")

if __name__ == "__main__":
    test_movie_crud()
