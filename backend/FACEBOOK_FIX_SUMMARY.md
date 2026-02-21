# Facebook Posts Not Appearing - FIXED

## Problem Identified ✅

Your Facebook posts are being scheduled in the database but **not appearing on Facebook** because:

**Your Facebook Page Access Token has EXPIRED**

```
Error: Session has expired on Friday, 20-Feb-26 17:00:00 PST
```

Facebook tokens expire after 60 days by default. Your token expired today.

## Why Posts Seemed to Work

The app was creating posts in the database successfully, but when it tried to send them to Facebook, the API call failed silently. The posts were marked as "scheduled" in your database but never actually posted to Facebook.

## Solution: Generate a New Token

### Quick Fix (5 minutes)

1. **Run the helper script:**
   ```bash
   cd backend
   python generate_facebook_token.py
   ```

2. **Follow the prompts:**
   - It will guide you through getting a new token
   - Automatically updates your .env file
   - Tests the new token

### Manual Fix (if script doesn't work)

1. Go to: https://developers.facebook.com/tools/explorer/

2. Select your app (ID: 1642741130093115)

3. Click "Generate Access Token"

4. Select permissions:
   - ✅ pages_manage_posts
   - ✅ pages_read_engagement

5. Click "Generate Access Token" and authorize

6. Make GET request to: `/me/accounts`

7. Find your page (ID: 1017037698154085)

8. Copy the `access_token` value

9. Update `backend/.env`:
   ```env
   FACEBOOK_PAGE_ACCESS_TOKEN=paste_new_token_here
   ```

10. Restart backend server

## Verify the Fix

After updating the token:

```bash
cd backend
python test_facebook_api.py
```

This will:
- ✅ Verify token is valid
- ✅ Check permissions
- ✅ Create a test post on Facebook
- ✅ Delete the test post

## What Changed

### Before (Broken)
```
User creates post → Saved to database → Facebook API call FAILS (expired token)
→ Post shows as "scheduled" but never appears on Facebook
```

### After (Fixed)
```
User creates post → Saved to database → Facebook API call SUCCESS (valid token)
→ Post appears on Facebook immediately (or at scheduled time)
```

## Preventing This in the Future

### Option 1: Set a Reminder
- Facebook tokens expire every 60 days
- Set a calendar reminder to refresh your token
- Run `python generate_facebook_token.py` every 2 months

### Option 2: Use Long-Lived Tokens
- Add `FB_APP_SECRET` to your .env file
- The helper script will automatically generate long-lived tokens
- These last 60 days instead of 1-2 hours

### Option 3: Implement Auto-Refresh (Future)
We can implement automatic token refresh:
- Monitor token expiration
- Send email alerts before expiration
- Auto-refresh tokens when possible

## Files Created to Help You

1. **test_facebook_api.py** - Diagnose Facebook API issues
2. **generate_facebook_token.py** - Generate new tokens easily
3. **FACEBOOK_TOKEN_GUIDE.md** - Detailed token generation guide
4. **FACEBOOK_FIX_SUMMARY.md** - This file

## Common Questions

**Q: Why did my posts show as "scheduled" if the token was expired?**
A: The app saves posts to the database first, then tries to send to Facebook. The database save succeeded, but the Facebook API call failed silently.

**Q: Will my old scheduled posts now appear on Facebook?**
A: No. Posts that failed to send are still in your database but were never sent to Facebook. You'll need to recreate them.

**Q: How often do I need to do this?**
A: Every 60 days for long-lived tokens, or every 1-2 hours for short-lived tokens.

**Q: Can I make a token that never expires?**
A: Yes! Page tokens from long-lived user tokens typically don't expire. The helper script will try to generate these automatically.

## Next Steps

1. ✅ Run `python generate_facebook_token.py`
2. ✅ Follow the prompts to get a new token
3. ✅ Run `python test_facebook_api.py` to verify
4. ✅ Restart your backend server
5. ✅ Try creating a new Facebook post
6. ✅ Check your Facebook page - it should appear!

## Need Help?

If you're still having issues:
1. Check the error messages in `test_facebook_api.py`
2. Verify your Page ID is correct: 1017037698154085
3. Make sure you have admin access to the Facebook page
4. Ensure your app is not in "Development Mode" (or add yourself as a test user)

---

**Status:** Issue identified and solution provided ✅
**Time to fix:** ~5 minutes
**Difficulty:** Easy (just run the helper script)
