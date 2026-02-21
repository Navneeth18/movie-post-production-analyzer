# Facebook Page Auto Poster

Production-ready Python automation to publish scheduled posts to a Facebook Page using the Facebook Graph API.

## Features
- Scheduled posting with `schedule`
- Supports message-only, link posts, and image posts (image URL upload + feed publish)
- Token validation and clear error messages for expiration/permission issues
- Retry logic for transient API/network failures
- Structured logging to `autopost.log`
- Token helper script to generate a long-lived Page token

## Project Structure
- `auto_post.py`: scheduler + posting logic
- `generate_page_token.py`: helper script to generate and validate long-lived tokens
- `config.json`: runtime config (Page ID, token, scheduled posts)
- `requirements.txt`: Python dependencies

## Prerequisites
1. Python 3.10+
2. A Facebook Page you manage
3. Facebook Developer account

## 1) Create a Facebook Developer App
1. Open: https://developers.facebook.com/
2. Create a new app (Business type is commonly used for Pages).
3. Add **Facebook Login** product.
4. Add **Graph API Explorer** access for testing.
5. In App Settings, note your:
   - `App ID`
   - `App Secret`

## 2) Required Permissions
Request and grant these permissions for the user token that manages the Page:
- `pages_show_list`
- `pages_manage_posts`
- `pages_read_engagement` (recommended)

Important:
- For production/public use, your app may need App Review for these permissions.
- For development mode, only app roles (admin/developer/tester) can use the app.

## 3) Generate Long-Lived Page Access Token
This project includes `generate_page_token.py` to guide this flow.

### Token Flow
1. Generate a **short-lived User Access Token** with required permissions.
2. Exchange it for a **long-lived User Access Token**.
3. Exchange the long-lived user token for a **Page Access Token**.

### Run helper script
```bash
python generate_page_token.py
```

## 4) Configure `config.json`
```json
{
  "page_id": "123456789012345",
  "page_access_token": "EAAB...",
  "posts": [
    {
      "message": "Good morning! Daily update posted automatically.",
      "scheduled_time": "09:00"
    },
    {
      "message": "Check this out",
      "link_url": "https://example.com/article",
      "scheduled_time": "13:30"
    },
    {
      "message": "New promo image",
      "image_url": "https://example.com/promo.jpg",
      "scheduled_time": "18:00"
    }
  ]
}
```

## 5) Install Dependencies
```bash
pip install -r requirements.txt
```

## 6) Run Scheduler
```bash
python auto_post.py
```

## 7) Test and Debug Tokens
- Built-in validation in `auto_post.py`
- Built-in debug in `generate_page_token.py`
- Facebook debugger: https://developers.facebook.com/tools/debug/accesstoken/

## Common Errors
- `code 190`: token invalid/expired
- `code 10` or `code 200`: missing permissions

## Security
- `config.json` contains sensitive token data
- Do not commit real tokens
- Rotate token if compromised