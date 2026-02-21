"""
Test Facebook API Connection
Run this to diagnose Facebook posting issues
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
PAGE_ID = os.getenv('FACEBOOK_PAGE_ID')

print("=" * 60)
print("Facebook API Connection Test")
print("=" * 60)

# Check if credentials are loaded
print("\n1. Checking Environment Variables:")
print(f"   PAGE_ID: {PAGE_ID if PAGE_ID else '❌ NOT FOUND'}")
print(f"   ACCESS_TOKEN: {'✅ Found' if PAGE_ACCESS_TOKEN else '❌ NOT FOUND'}")

if not PAGE_ACCESS_TOKEN or not PAGE_ID:
    print("\n❌ ERROR: Missing credentials in .env file")
    print("\nMake sure your .env file has:")
    print("   FACEBOOK_PAGE_ACCESS_TOKEN=your_token")
    print("   FACEBOOK_PAGE_ID=your_page_id")
    exit(1)

# Test 1: Verify token and get page info
print("\n2. Testing Token Validity:")
try:
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}"
    params = {
        'fields': 'id,name,access_token',
        'access_token': PAGE_ACCESS_TOKEN
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Token is valid!")
        print(f"   Page Name: {data.get('name')}")
        print(f"   Page ID: {data.get('id')}")
    else:
        print(f"   ❌ Token validation failed!")
        print(f"   Status: {response.status_code}")
        print(f"   Error: {response.json()}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Check token permissions
print("\n3. Checking Token Permissions:")
try:
    url = "https://graph.facebook.com/v18.0/me/permissions"
    params = {'access_token': PAGE_ACCESS_TOKEN}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        permissions = response.json().get('data', [])
        required_perms = ['pages_manage_posts', 'pages_read_engagement']
        
        granted = [p['permission'] for p in permissions if p['status'] == 'granted']
        print(f"   Granted permissions: {', '.join(granted)}")
        
        missing = [p for p in required_perms if p not in granted]
        if missing:
            print(f"   ⚠️  Missing permissions: {', '.join(missing)}")
            print(f"   You may need to regenerate your token with these permissions")
        else:
            print(f"   ✅ All required permissions granted!")
    else:
        print(f"   ⚠️  Could not check permissions: {response.status_code}")
except Exception as e:
    print(f"   ⚠️  Error checking permissions: {e}")

# Test 3: Try to create a test post
print("\n4. Testing Post Creation:")
test_message = "🎬 Test post from Movie PR System - Please ignore! 🎬"

try:
    url = f"https://graph.facebook.com/v18.0/{PAGE_ID}/feed"
    params = {
        'access_token': PAGE_ACCESS_TOKEN,
        'message': test_message
    }
    
    response = requests.post(url, params=params)
    
    if response.status_code == 200:
        post_data = response.json()
        post_id = post_data.get('id')
        print(f"   ✅ Test post created successfully!")
        print(f"   Post ID: {post_id}")
        
        # Try to delete the test post
        delete_url = f"https://graph.facebook.com/v18.0/{post_id}"
        delete_params = {'access_token': PAGE_ACCESS_TOKEN}
        delete_response = requests.delete(delete_url, params=delete_params)
        
        if delete_response.status_code == 200:
            print(f"   ✅ Test post deleted successfully!")
        else:
            print(f"   ⚠️  Could not delete test post (you may need to delete it manually)")
    else:
        print(f"   ❌ Post creation failed!")
        print(f"   Status: {response.status_code}")
        error_data = response.json()
        print(f"   Error: {error_data}")
        
        # Common error explanations
        if 'error' in error_data:
            error_code = error_data['error'].get('code')
            error_msg = error_data['error'].get('message')
            
            print(f"\n   Error Code: {error_code}")
            print(f"   Message: {error_msg}")
            
            if error_code == 190:
                print("\n   💡 Solution: Your access token is invalid or expired.")
                print("      Generate a new Page Access Token from Facebook Graph API Explorer")
            elif error_code == 200:
                print("\n   💡 Solution: Missing required permissions.")
                print("      Regenerate token with 'pages_manage_posts' permission")
            elif error_code == 100:
                print("\n   💡 Solution: Invalid parameter or Page ID.")
                print("      Verify your FACEBOOK_PAGE_ID is correct")

except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
