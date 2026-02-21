# Facebook Campaign Automation Module

## Overview
Automated Facebook posting and campaign management for movie PR. This module helps producers create, schedule, and manage Facebook posts for their upcoming movies.

## Features

### 1. **Content Generation**
Automatically generates Facebook post content for different campaign types:
- **Teaser**: Initial mysterious posts to build anticipation
- **Trailer**: Trailer release announcements
- **Cast Reveal**: Star cast announcements
- **Countdown**: Daily countdown posts (30, 15, 10, 7, 3, 1 days)
- **Release**: Release day announcements

### 2. **Post Scheduling**
- Schedule posts for future dates
- Create complete campaign schedules automatically
- Manage scheduled posts

### 3. **Analytics**
- Track post impressions
- Monitor engagement (likes, comments, shares)
- View click-through rates

### 4. **Campaign Planning**
- Generate 30-day campaign schedules
- Automatic milestone posts
- Customizable campaign duration

## Restrictions

✅ **Available for**: Current/unreleased movies only (tag="current")
❌ **Not available for**: Historical movies (tag="past")

## API Endpoints

### Base URL: `/api/v1/facebook-campaign`

### 1. Generate Content
```http
POST /{movie_id}/generate-content
```

**Request:**
```json
{
  "campaign_type": "teaser"  // teaser, trailer, countdown, release, cast_reveal
}
```

**Response:**
```json
{
  "message": "🎬 Something BIG is coming! 🎬\n\nGet ready for Baahubali...",
  "hashtags": ["#Baahubali", "#SSRajamouli", "#MovieRelease"],
  "suggestion": "Post a mysterious image or short teaser clip",
  "campaign_type": "teaser"
}
```

### 2. Create/Schedule Post
```http
POST /{movie_id}/create-post
```

**Request:**
```json
{
  "message": "Post content here",
  "link": "https://youtube.com/trailer",  // optional
  "image_url": "https://example.com/poster.jpg",  // optional
  "scheduled_time": "2024-03-15T10:00:00Z"  // optional
}
```

**Response:**
```json
{
  "success": true,
  "post_id": "123456789",
  "scheduled": true,
  "scheduled_time": "2024-03-15T10:00:00Z",
  "mock": false
}
```

### 3. Get Campaign Schedule
```http
GET /{movie_id}/campaign-schedule?campaign_duration_days=30
```

**Response:**
```json
[
  {
    "title": "Initial Teaser",
    "scheduled_date": "2024-02-15T10:00:00Z",
    "campaign_type": "teaser",
    "message": "Post content...",
    "hashtags": ["#MovieName"],
    "suggestion": "Post a mysterious image",
    "status": "pending"
  },
  ...
]
```

### 4. Get Movie Posts
```http
GET /{movie_id}/posts
```

**Response:**
```json
[
  {
    "id": "post_doc_id",
    "post_id": "fb_post_id",
    "message": "Post content",
    "scheduled_time": "2024-03-15T10:00:00Z",
    "created_at": "2024-03-01T10:00:00Z",
    "status": "scheduled",
    "mock": false
  }
]
```

### 5. Get Post Insights
```http
GET /post/{post_id}/insights
```

**Response:**
```json
{
  "success": true,
  "impressions": 15000,
  "engaged_users": 1200,
  "clicks": 450,
  "mock": false
}
```

### 6. Delete Scheduled Post
```http
DELETE /post/{post_id}
```

## Configuration

### Environment Variables

Add to `.env`:
```env
# Facebook API (optional - uses mock data if not set)
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id

# Optional (for token generation)
FB_APP_ID=your_app_id
FB_APP_SECRET=your_app_secret
FB_SHORT_USER_TOKEN=your_short_lived_token

# Pollinations AI (for image generation)
POLLINATIONS_API_KEY=your_pollinations_api_key
```

**Note**: The service uses `FACEBOOK_PAGE_ACCESS_TOKEN` and `FACEBOOK_PAGE_ID` (not `FACEBOOK_ACCESS_TOKEN`).

### Getting Facebook Credentials

1. **Create Facebook App**:
   - Go to https://developers.facebook.com/
   - Create a new app
   - Add "Pages" product

2. **Get Page Access Token**:
   - Go to Graph API Explorer
   - Select your app
   - Select your page
   - Generate access token with permissions:
     - `pages_manage_posts`
     - `pages_read_engagement`
     - `pages_manage_metadata`

3. **Get Page ID**:
   - Go to your Facebook page
   - Settings → About
   - Copy Page ID

## Mock Mode

If Facebook credentials are not configured, the module operates in **mock mode**:
- Posts are "created" but not actually posted to Facebook
- Mock analytics data is returned
- All functionality works for testing
- Posts are stored in database with `mock: true` flag

## Campaign Types

### 1. Teaser
- **When**: 30 days before release
- **Purpose**: Build anticipation
- **Content**: Mysterious, intriguing
- **Suggestion**: Post teaser images/clips

### 2. Cast Reveal
- **When**: 25 days before release
- **Purpose**: Announce star cast
- **Content**: Cast names and roles
- **Suggestion**: Post cast photos

### 3. Trailer
- **When**: 20 days before release
- **Purpose**: Release official trailer
- **Content**: Trailer announcement
- **Suggestion**: Post trailer video

### 4. Countdown
- **When**: 15, 10, 7, 3, 1 days before
- **Purpose**: Build excitement
- **Content**: Days remaining
- **Suggestion**: Countdown graphics

### 5. Release
- **When**: Release day
- **Purpose**: Announce availability
- **Content**: "Now in theaters!"
- **Suggestion**: Release poster

## Database Collections

### `facebook_posts`
```json
{
  "movie_id": "movie_object_id",
  "producer_id": "user_object_id",
  "post_id": "facebook_post_id",
  "message": "Post content",
  "link": "optional_url",
  "image_url": "optional_image",
  "scheduled_time": "datetime",
  "created_at": "datetime",
  "status": "scheduled|posted|failed",
  "mock": false
}
```

## Usage Example

### 1. Generate Campaign Schedule
```javascript
const schedule = await facebookCampaignAPI.getCampaignSchedule(movieId, 30);
// Returns 9 scheduled posts over 30 days
```

### 2. Create Custom Post
```javascript
const content = await facebookCampaignAPI.generateContent(movieId, 'teaser');
const post = await facebookCampaignAPI.createPost(movieId, {
  message: content.message,
  image_url: 'https://example.com/poster.jpg',
  scheduled_time: '2024-03-15T10:00:00Z'
});
```

### 3. View Analytics
```javascript
const insights = await facebookCampaignAPI.getPostInsights(postId);
console.log(`Impressions: ${insights.impressions}`);
console.log(`Engagement: ${insights.engaged_users}`);
```

## Frontend Integration

✅ **Complete** - Facebook Campaign page is fully implemented!

### Access
1. Navigate to any current movie's detail page
2. Click "Facebook Campaign" button (only visible for current movies)
3. Use the campaign management interface

### Features
- **Create Post Tab**: Generate and customize posts
- **Campaign Schedule Tab**: View 30-day campaign plan
- **My Posts Tab**: Track all created/scheduled posts

### Route
```
/movies/:id/facebook-campaign
```

### Components
- `src/pages/FacebookCampaign.jsx` - Main campaign page
- `src/pages/MovieDetail.jsx` - Button integration
- `src/services/api.js` - API methods
- `src/App.jsx` - Route configuration

## Benefits

1. **Automated Content**: AI-generated posts for different campaign stages
2. **Scheduling**: Plan entire campaign in advance
3. **Analytics**: Track performance of each post
4. **Time-Saving**: No manual posting needed
5. **Consistency**: Regular, scheduled updates
6. **Professional**: Well-formatted posts with hashtags

## Security

- All endpoints require authentication
- Producer ownership verified
- Only current movies can use campaigns
- Facebook API credentials stored securely in environment variables

## Testing

Without Facebook API credentials, the module works in mock mode:
- All endpoints return success
- Mock data for analytics
- Posts stored in database
- Perfect for development/testing

## Future Enhancements

- [ ] Instagram integration
- [ ] Twitter/X integration
- [ ] AI-powered content optimization
- [ ] A/B testing for posts
- [ ] Audience targeting
- [ ] Budget tracking
- [ ] ROI analytics
