# Facebook Access Token - Setup Guide

## Problem
Your Facebook Page Access Token has **expired**. Facebook tokens expire after 60 days by default.

**Error Message:**
```
Session has expired on Friday, 20-Feb-26 17:00:00 PST
```

## Solution: Generate a New Page Access Token

### Method 1: Quick Token (Expires in 1-2 hours) - For Testing

1. Go to [Facebook Graph API Explorer](https://developers.facebook.com/tools/explorer/)

2. Select your App from the dropdown (top right)

3. Click "Generate Access Token"

4. Select these permissions:
   - `pages_manage_posts` (required)
   - `pages_read_engagement` (required)
   - `pages_manage_metadata` (optional)

5. Click "Generate Access Token" and authorize

6. You'll get a **User Access Token**

7. To convert it to a **Page Access Token**:
   - In the Graph API Explorer, make a GET request to:
   ```
   /me/accounts
   ```
   - Find your page in the response
   - Copy the `access_token` for your page
   - This is your Page Access Token

8. Update your `.env` file:
   ```env
   FACEBOOK_PAGE_ACCESS_TOKEN=your_new_page_token_here
   ```

### Method 2: Long-Lived Token (Expires in 60 days) - Recommended

1. Get a short-lived User Access Token (follow Method 1, steps 1-5)

2. Exchange it for a long-lived token using this URL:
   ```
   https://graph.facebook.com/v18.0/oauth/access_token?
     grant_type=fb_exchange_token&
     client_id=YOUR_APP_ID&
     client_secret=YOUR_APP_SECRET&
     fb_exchange_token=YOUR_SHORT_LIVED_TOKEN
   ```

3. Use the long-lived User Token to get a long-lived Page Token:
   ```
   https://graph.facebook.com/v18.0/me/accounts?
     access_token=YOUR_LONG_LIVED_USER_TOKEN
   ```

4. Copy the Page Access Token from the response

5. Update your `.env` file

### Method 3: Never-Expiring Token (Best for Production)

**Note:** This requires your app to be in "Live" mode (not Development mode)

1. Follow Method 2 to get a long-lived Page Token

2. The Page Token from a long-lived User Token typically doesn't expire

3. Verify it doesn't expire by checking:
   ```
   https://graph.facebook.com/v18.0/debug_token?
     input_token=YOUR_PAGE_TOKEN&
     access_token=YOUR_APP_TOKEN
   ```

4. Look for `expires_at: 0` (means never expires)

## Using the Helper Script

We've created a helper script to generate tokens:

```bash
cd backend
python generate_facebook_token.py
```

This script will:
1. Check your current token status
2. Guide you through generating a new token
3. Test the new token
4. Update your .env file

## Required Permissions

Your Page Access Token must have these permissions:
- ✅ `pages_manage_posts` - To create posts
- ✅ `pages_read_engagement` - To read analytics
- ⚠️ `pages_manage_metadata` - Optional, for advanced features

## Common Issues

### Issue 1: Token Expired
**Solution:** Generate a new token using Method 1 or 2

### Issue 2: Missing Permissions
**Error:** `(#200) Requires extended permission: pages_manage_posts`
**Solution:** Regenerate token with correct permissions

### Issue 3: Invalid Page ID
**Error:** `(#100) Invalid parameter`
**Solution:** Verify your `FACEBOOK_PAGE_ID` in .env

### Issue 4: App Not Approved
**Error:** `This app is in Development Mode`
**Solution:** 
- For testing: Add your Facebook account as a test user
- For production: Submit app for review

## Testing Your Token

After updating the token, test it:

```bash
cd backend
python test_facebook_api.py
```

This will:
1. ✅ Verify token is valid
2. ✅ Check permissions
3. ✅ Create a test post
4. ✅ Delete the test post

## Environment Variables

Your `.env` file should have:

```env
# Facebook Page Credentials
FACEBOOK_PAGE_ID=1017037698154085
FACEBOOK_PAGE_ACCESS_TOKEN=your_new_token_here

# Optional (for token generation)
FB_APP_ID=1642741130093115
FB_APP_SECRET=your_app_secret
```

## Quick Fix (Right Now)

1. Go to: https://developers.facebook.com/tools/explorer/

2. Select your app: "1642741130093115"

3. Click "Generate Access Token"

4. Select permissions: `pages_manage_posts`, `pages_read_engagement`

5. Authorize

6. Make GET request to: `/me/accounts`

7. Find your page (ID: 1017037698154085)

8. Copy the `access_token` value

9. Update `backend/.env`:
   ```env
   FACEBOOK_PAGE_ACCESS_TOKEN=paste_token_here
   ```

10. Restart your backend server

11. Test by creating a post!

## Automatic Token Refresh (Future Enhancement)

To avoid this issue in the future, we can implement:
- Automatic token refresh before expiration
- Email notifications when token is about to expire
- OAuth flow for users to connect their own Facebook pages

Would you like me to implement automatic token refresh?
