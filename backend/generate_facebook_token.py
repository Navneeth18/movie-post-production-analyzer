"""
Facebook Token Generator Helper
Helps you generate and test Facebook Page Access Tokens
"""
import os
import requests
from dotenv import load_dotenv, set_key

load_dotenv()

def check_current_token():
    """Check if current token is valid"""
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    if not token or not page_id:
        return False, "No token found in .env"
    
    try:
        url = f"https://graph.facebook.com/v18.0/{page_id}"
        params = {'access_token': token, 'fields': 'id,name'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return True, "Token is valid"
        else:
            error = response.json().get('error', {})
            return False, error.get('message', 'Token invalid')
    except Exception as e:
        return False, str(e)

def debug_token(token):
    """Get token information"""
    try:
        url = "https://graph.facebook.com/v18.0/debug_token"
        params = {
            'input_token': token,
            'access_token': token
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            return data
        return None
    except:
        return None

def get_page_token_from_user_token(user_token):
    """Convert user token to page token"""
    try:
        url = "https://graph.facebook.com/v18.0/me/accounts"
        params = {'access_token': user_token}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            pages = response.json().get('data', [])
            return pages
        return None
    except:
        return None

def exchange_for_long_lived_token(short_token, app_id, app_secret):
    """Exchange short-lived token for long-lived token"""
    try:
        url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            'grant_type': 'fb_exchange_token',
            'client_id': app_id,
            'client_secret': app_secret,
            'fb_exchange_token': short_token
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('access_token')
        return None
    except:
        return None

def main():
    print("=" * 70)
    print("Facebook Page Access Token Generator")
    print("=" * 70)
    
    # Check current token
    print("\n1. Checking current token...")
    is_valid, message = check_current_token()
    
    if is_valid:
        print(f"   ✅ {message}")
        print("\n   Your current token is working! No need to generate a new one.")
        return
    else:
        print(f"   ❌ {message}")
        print("   You need to generate a new token.")
    
    # Get configuration
    page_id = os.getenv('FACEBOOK_PAGE_ID')
    app_id = os.getenv('FB_APP_ID')
    app_secret = os.getenv('FB_APP_SECRET')
    
    print(f"\n2. Configuration:")
    print(f"   Page ID: {page_id if page_id else '❌ Not set'}")
    print(f"   App ID: {app_id if app_id else '❌ Not set'}")
    print(f"   App Secret: {'✅ Set' if app_secret else '❌ Not set'}")
    
    # Guide user through token generation
    print("\n" + "=" * 70)
    print("STEP-BY-STEP GUIDE")
    print("=" * 70)
    
    print("\n📋 Step 1: Get a User Access Token")
    print("   1. Go to: https://developers.facebook.com/tools/explorer/")
    print(f"   2. Select your app (ID: {app_id if app_id else 'YOUR_APP_ID'})")
    print("   3. Click 'Generate Access Token'")
    print("   4. Select these permissions:")
    print("      ✓ pages_manage_posts")
    print("      ✓ pages_read_engagement")
    print("   5. Click 'Generate Access Token' and authorize")
    print("   6. Copy the token shown")
    
    user_token = input("\n   Paste your User Access Token here: ").strip()
    
    if not user_token:
        print("\n   ❌ No token provided. Exiting.")
        return
    
    # Try to get page token
    print("\n📋 Step 2: Converting to Page Access Token...")
    pages = get_page_token_from_user_token(user_token)
    
    if not pages:
        print("   ❌ Could not get pages. Make sure your token has the right permissions.")
        return
    
    print(f"   ✅ Found {len(pages)} page(s):")
    for i, page in enumerate(pages, 1):
        print(f"      {i}. {page['name']} (ID: {page['id']})")
    
    # Find the target page
    target_page = None
    if page_id:
        target_page = next((p for p in pages if p['id'] == page_id), None)
    
    if not target_page:
        if len(pages) == 1:
            target_page = pages[0]
        else:
            choice = input(f"\n   Select page number (1-{len(pages)}): ").strip()
            try:
                target_page = pages[int(choice) - 1]
            except:
                print("   ❌ Invalid choice. Exiting.")
                return
    
    page_token = target_page['access_token']
    page_name = target_page['name']
    page_id_found = target_page['id']
    
    print(f"\n   ✅ Got Page Access Token for: {page_name}")
    
    # Check if we can make it long-lived
    if app_id and app_secret:
        print("\n📋 Step 3: Converting to Long-Lived Token...")
        long_lived = exchange_for_long_lived_token(user_token, app_id, app_secret)
        
        if long_lived:
            print("   ✅ Got long-lived User Token")
            
            # Get long-lived page token
            pages_ll = get_page_token_from_user_token(long_lived)
            if pages_ll:
                target_ll = next((p for p in pages_ll if p['id'] == page_id_found), None)
                if target_ll:
                    page_token = target_ll['access_token']
                    print("   ✅ Got long-lived Page Token (lasts 60 days)")
        else:
            print("   ⚠️  Could not get long-lived token. Using short-lived token.")
    else:
        print("\n   ⚠️  App Secret not configured. Using short-lived token.")
        print("      Add FB_APP_SECRET to .env for long-lived tokens.")
    
    # Debug token info
    print("\n📋 Step 4: Token Information...")
    token_info = debug_token(page_token)
    if token_info:
        expires_at = token_info.get('expires_at', 0)
        if expires_at == 0:
            print("   ✅ Token never expires!")
        else:
            from datetime import datetime
            expiry = datetime.fromtimestamp(expires_at)
            print(f"   ⏰ Token expires: {expiry}")
    
    # Test the token
    print("\n📋 Step 5: Testing Token...")
    try:
        url = f"https://graph.facebook.com/v18.0/{page_id_found}"
        params = {'access_token': page_token, 'fields': 'id,name'}
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            print("   ✅ Token works!")
        else:
            print(f"   ❌ Token test failed: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error testing token: {e}")
        return
    
    # Update .env file
    print("\n📋 Step 6: Updating .env file...")
    env_path = '.env'
    
    try:
        set_key(env_path, 'FACEBOOK_PAGE_ACCESS_TOKEN', page_token)
        set_key(env_path, 'FACEBOOK_PAGE_ID', page_id_found)
        print("   ✅ .env file updated!")
    except Exception as e:
        print(f"   ⚠️  Could not update .env automatically: {e}")
        print(f"\n   Please manually update your .env file:")
        print(f"   FACEBOOK_PAGE_ACCESS_TOKEN={page_token}")
        print(f"   FACEBOOK_PAGE_ID={page_id_found}")
    
    print("\n" + "=" * 70)
    print("✅ SUCCESS! Your Facebook token is ready!")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Restart your backend server")
    print("2. Try creating a Facebook post from your app")
    print("3. Run 'python test_facebook_api.py' to verify everything works")
    print("\n💡 Tip: Set a reminder to refresh your token in 60 days!")

if __name__ == "__main__":
    main()
