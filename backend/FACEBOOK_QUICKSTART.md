# Facebook Campaign - Quick Start Guide

## Issue: Posts Not Appearing on Facebook

Your Facebook Page Access Token has **expired**. This is why posts are being saved in the database but not appearing on Facebook.

## Fix It Now (5 Minutes)

### Step 1: Generate New Token

```bash
cd backend
python generate_facebook_token.py
```

The script will:
1. ✅ Check your current token (expired)
2. ✅ Guide you through getting a new token
3. ✅ Test the new token
4. ✅ Update your .env file automatically

### Step 2: Follow the Prompts

When the script asks for a User Access Token:

1. Open: https://developers.facebook.com/tools/explorer/
2. Select your app (ID: 1642741130093115)
3. Click "Generate Access Token"
4. Select permissions:
   - ✅ pages_manage_posts
   - ✅ pages_read_engagement
5. Click "Generate Access Token" and authorize
6. Copy the token
7. Paste it into the terminal

The script will automatically:
- Convert it to a Page Access Token
- Make it long-lived (60 days)
- Update your .env file
- Test that it works

### Step 3: Restart Backend

```bash
# Stop your backend (Ctrl+C)
# Then restart it
uvicorn app.main:app --reload
```

### Step 4: Test It

```bash
python test_facebook_api.py
```

You should see:
```
✅ Token is valid!
✅ All required permissions granted!
✅ Test post created successfully!
✅ Test post deleted successfully!
```

### Step 5: Create a Post

1. Go to your app
2. Navigate to a current movie
3. Click "Facebook Campaign"
4. Create a post
5. Check your Facebook page - it should appear!

## Alternative: Manual Token Update

If the script doesn't work, manually update your token:

1. Get token from: https://developers.facebook.com/tools/explorer/
2. Make GET request to: `/me/accounts`
3. Copy the `access_token` for your page
4. Update `backend/.env`:
   ```env
   FACEBOOK_PAGE_ACCESS_TOKEN=your_new_token_here
   ```
5. Restart backend

## Verify Everything Works

After fixing:

```bash
# Test the API
python test_facebook_api.py

# Should show:
# ✅ Token is valid!
# ✅ Test post created successfully!
```

## Why This Happened

Facebook tokens expire after 60 days. Your token expired on Feb 20, 2026 at 5:00 PM PST.

## Prevent Future Issues

### Option 1: Calendar Reminder
Set a reminder to refresh your token every 60 days.

### Option 2: Long-Lived Tokens
Add `FB_APP_SECRET` to your .env file. The helper script will automatically generate long-lived tokens.

### Option 3: Never-Expiring Tokens
Page tokens from long-lived user tokens typically don't expire. The helper script tries to generate these automatically.

## Troubleshooting

### "Token validation failed"
- Your token is expired or invalid
- Run `python generate_facebook_token.py` to get a new one

### "Missing permissions"
- Your token doesn't have required permissions
- Regenerate with `pages_manage_posts` permission

### "Invalid Page ID"
- Check your `FACEBOOK_PAGE_ID` in .env
- Should be: 1017037698154085

### "App is in Development Mode"
- Add yourself as a test user in Facebook App settings
- Or switch app to Live mode (requires review)

## Files to Help You

- `generate_facebook_token.py` - Generate new tokens easily
- `test_facebook_api.py` - Test your Facebook connection
- `FACEBOOK_TOKEN_GUIDE.md` - Detailed token guide
- `FACEBOOK_FIX_SUMMARY.md` - Full explanation of the issue

## Need Help?

Run the diagnostic script:
```bash
python test_facebook_api.py
```

It will tell you exactly what's wrong and how to fix it.

---

**TL;DR:**
1. Run `python generate_facebook_token.py`
2. Follow the prompts
3. Restart backend
4. Posts will now appear on Facebook ✅
