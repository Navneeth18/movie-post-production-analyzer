"""
Test Facebook Image Upload (Download then Upload method)
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

print("=" * 70)
print("Facebook Image Upload Test (Download & Upload)")
print("=" * 70)

# Test: Download image and upload to Facebook
print("\n1. Testing download and upload method...")
try:
    # Use a simple, reliable image URL
    image_url = "https://picsum.photos/1024/1024"
    
    print(f"   Downloading image from: {image_url}")
    img_response = requests.get(image_url, timeout=30)
    img_response.raise_for_status()
    
    print(f"   ✅ Image downloaded ({len(img_response.content)} bytes)")
    print(f"   Content-Type: {img_response.headers.get('Content-Type')}")
    
    # Upload to Facebook
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/photos"
    
    files = {
        'source': ('image.jpg', img_response.content, 'image/jpeg')
    }
    
    data = {
        'access_token': PAGE_ACCESS_TOKEN,
        'caption': 'Test post with uploaded image'
    }
    
    print(f"   Uploading to Facebook...")
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        post_id = response.json().get('id')
        print(f"   ✅ Image post created: {post_id}")
        print(f"   Check your Facebook page!")
        
        # Delete it
        delete_response = requests.delete(
            f"https://graph.facebook.com/v18.0/{post_id}",
            params={'access_token': PAGE_ACCESS_TOKEN}
        )
        if delete_response.status_code == 200:
            print(f"   ✅ Test post deleted")
        else:
            print(f"   ⚠️  Could not delete test post (you may need to delete manually)")
    else:
        error_data = response.json()
        print(f"   ❌ Failed: {error_data}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 70)
print("Test Complete!")
print("=" * 70)
