"""
Test Facebook Post with Image
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

print("=" * 70)
print("Facebook Post with Image Test")
print("=" * 70)

# Test 1: Post with text only
print("\n1. Testing text-only post...")
try:
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    params = {
        'access_token': PAGE_ACCESS_TOKEN,
        'message': 'Test text-only post'
    }
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        post_id = response.json().get('id')
        print(f"   ✅ Text post created: {post_id}")
        
        # Delete it
        requests.delete(f"https://graph.facebook.com/v18.0/{post_id}", params={'access_token': PAGE_ACCESS_TOKEN})
        print(f"   ✅ Test post deleted")
    else:
        print(f"   ❌ Failed: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Post with image URL
print("\n2. Testing post with image...")
try:
    # Use a Pollinations generated image
    image_url = "https://image.pollinations.ai/prompt/Cinematic%20movie%20poster%2C%20action%20genre%2C%20professional%20style?width=1024&height=1024&nologo=true"
    
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
    params = {
        'access_token': PAGE_ACCESS_TOKEN,
        'url': image_url,
        'caption': 'Test post with AI-generated image'
    }
    
    print(f"   Image URL: {image_url}")
    print(f"   Posting to: {url}")
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        post_id = response.json().get('id')
        print(f"   ✅ Image post created: {post_id}")
        
        # Delete it
        requests.delete(f"https://graph.facebook.com/v18.0/{post_id}", params={'access_token': PAGE_ACCESS_TOKEN})
        print(f"   ✅ Test post deleted")
    else:
        error_data = response.json()
        print(f"   ❌ Failed: {error_data}")
        
        error = error_data.get('error', {})
        print(f"\n   Error Code: {error.get('code')}")
        print(f"   Error Type: {error.get('type')}")
        print(f"   Message: {error.get('message')}")
        
        if error.get('code') == 100:
            print("\n   💡 This is an 'Invalid parameter' error")
            print("   Possible causes:")
            print("   - Image URL is not accessible")
            print("   - Image format not supported")
            print("   - Page ID is incorrect")
            print("   - Token doesn't have photo posting permission")
            
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Verify image URL is accessible
print("\n3. Testing if image URL is accessible...")
try:
    image_url = "https://image.pollinations.ai/prompt/Test%20movie%20poster?width=1024&height=1024&nologo=true"
    response = requests.get(image_url, timeout=10)
    
    if response.status_code == 200:
        print(f"   ✅ Image URL is accessible")
        print(f"   Content-Type: {response.headers.get('Content-Type')}")
        print(f"   Content-Length: {len(response.content)} bytes")
    else:
        print(f"   ❌ Image URL returned status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error accessing image: {e}")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
