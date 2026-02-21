"""
Test script for Facebook Campaign endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# You'll need to replace these with actual values
TEST_MOVIE_ID = "your_movie_id_here"
AUTH_TOKEN = "your_auth_token_here"

headers = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def test_generate_content():
    """Test content generation"""
    print("\n=== Testing Content Generation ===")
    url = f"{BASE_URL}/facebook-campaign/{TEST_MOVIE_ID}/generate-content"
    data = {"campaign_type": "teaser"}
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_create_post():
    """Test post creation"""
    print("\n=== Testing Post Creation ===")
    url = f"{BASE_URL}/facebook-campaign/{TEST_MOVIE_ID}/create-post"
    data = {
        "message": "Test post from API",
        "link": None,
        "image_url": None,
        "scheduled_time": None
    }
    
    response = requests.post(url, json=data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error: {response.text}")

def test_get_campaign_schedule():
    """Test campaign schedule generation"""
    print("\n=== Testing Campaign Schedule ===")
    url = f"{BASE_URL}/facebook-campaign/{TEST_MOVIE_ID}/campaign-schedule"
    params = {"campaign_duration_days": 30}
    
    response = requests.get(url, params=params, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        schedule = response.json()
        print(f"Generated {len(schedule)} posts")
        for post in schedule[:3]:  # Show first 3
            print(f"\n- {post['title']}")
            print(f"  Date: {post['scheduled_date']}")
            print(f"  Type: {post['campaign_type']}")
    else:
        print(f"Error: {response.text}")

def test_get_posts():
    """Test getting movie posts"""
    print("\n=== Testing Get Posts ===")
    url = f"{BASE_URL}/facebook-campaign/{TEST_MOVIE_ID}/posts"
    
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        posts = response.json()
        print(f"Found {len(posts)} posts")
        for post in posts[:3]:  # Show first 3
            print(f"\n- {post.get('message', '')[:50]}...")
            print(f"  Status: {post.get('status')}")
            print(f"  Mock: {post.get('mock', False)}")
    else:
        print(f"Error: {response.text}")

if __name__ == "__main__":
    print("Facebook Campaign API Test")
    print("=" * 50)
    print("\nNOTE: Update TEST_MOVIE_ID and AUTH_TOKEN before running")
    print("\nTo get auth token:")
    print("1. Login via /api/v1/auth/login")
    print("2. Copy the access_token from response")
    print("\nTo get movie ID:")
    print("1. Get movies via /api/v1/movies/all")
    print("2. Copy the _id of a current movie (tag='current')")
    
    # Uncomment to run tests (after setting TEST_MOVIE_ID and AUTH_TOKEN)
    # test_generate_content()
    # test_create_post()
    # test_get_campaign_schedule()
    # test_get_posts()
