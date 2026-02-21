"""Diagnose API routes"""
import requests

BASE_URL = "http://localhost:8000"

def diagnose():
    print("API Route Diagnostics")
    print("=" * 70)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print("   ⚠️  Backend server might not be running!")
        return
    
    # Test health endpoint
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test OpenAPI docs
    print("\n3. Checking available routes...")
    try:
        response = requests.get(f"{BASE_URL}/openapi.json")
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get("paths", {})
            
            print(f"   Found {len(paths)} route paths")
            print("\n   Movie-related routes:")
            for path in sorted(paths.keys()):
                if "/movies" in path:
                    methods = list(paths[path].keys())
                    print(f"     {path} - {', '.join(methods).upper()}")
        else:
            print(f"   ❌ Failed to get OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test auth endpoint
    print("\n4. Testing auth endpoint...")
    try:
        response = requests.post(f"{BASE_URL}/api/v1/auth/login", json={
            "email": "dilraju@gmail.com",
            "password": "123456"
        })
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Auth working")
            token = response.json()["access_token"]
            
            # Test movies list
            print("\n5. Testing movies list endpoint...")
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.get(f"{BASE_URL}/api/v1/movies/", headers=headers)
            print(f"   Status: {response.status_code}")
            if response.status_code == 200:
                movies = response.json()
                print(f"   ✅ Found {len(movies)} movies")
                
                if movies:
                    movie_id = movies[0]["id"]
                    print(f"\n6. Testing movie detail endpoint with ID: {movie_id}")
                    response = requests.get(f"{BASE_URL}/api/v1/movies/{movie_id}", headers=headers)
                    print(f"   Status: {response.status_code}")
                    if response.status_code == 200:
                        print("   ✅ Movie detail endpoint working!")
                    else:
                        print(f"   ❌ Movie detail failed: {response.text}")
            else:
                print(f"   ❌ Movies list failed: {response.text}")
        else:
            print(f"   ❌ Auth failed: {response.text}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("\nDiagnostics complete!")
    print("\nIf you see errors:")
    print("1. Make sure backend is running: uvicorn app.main:app --reload")
    print("2. Check MongoDB is running")
    print("3. Restart the backend server to load route changes")

if __name__ == "__main__":
    diagnose()
