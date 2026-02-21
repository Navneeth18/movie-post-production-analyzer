# Facebook Campaign Module - Usage Guide

## Overview
The Facebook Campaign module automates PR campaigns for unreleased movies. It helps producers create, schedule, and track Facebook posts for movie promotions.

## Features

### 1. Campaign Content Generation
- **Teaser**: Mysterious announcements to build anticipation
- **Trailer**: Official trailer releases with engagement prompts
- **Cast Reveal**: Star cast announcements with character details
- **Countdown**: Time-based posts counting down to release
- **Release Day**: Launch day announcements with theater info

### 2. Post Management
- Create immediate posts or schedule for future
- Attach images and links
- Auto-generate hashtags based on movie data
- Track post status (posted/scheduled)

### 3. Campaign Scheduling
- Generate complete 30-day campaign schedule
- Automated milestone posts at strategic intervals
- Customizable campaign duration

### 4. Analytics (when using real Facebook API)
- Post impressions
- Engaged users
- Click-through rates

## Restrictions
- **Only for unreleased movies** (tag="current")
- Historical movies (tag="past") cannot use this feature

## API Endpoints

### Generate Campaign Content
```
POST /api/v1/facebook-campaign/{movie_id}/generate-content
Body: { "campaign_type": "teaser" }
```

### Create/Schedule Post
```
POST /api/v1/facebook-campaign/{movie_id}/create-post
Body: {
  "message": "Post content",
  "image_url": "https://...",
  "link": "https://...",
  "scheduled_time": "2024-12-25T10:00:00"  // optional
}
```

### Get Campaign Schedule
```
GET /api/v1/facebook-campaign/{movie_id}/campaign-schedule?campaign_duration_days=30
```

### Get Movie Posts
```
GET /api/v1/facebook-campaign/{movie_id}/posts
```

### Get Post Insights
```
GET /api/v1/facebook-campaign/post/{post_id}/insights
```

### Delete Scheduled Post
```
DELETE /api/v1/facebook-campaign/post/{post_id}
```

## Environment Variables

Required for real Facebook API integration:
```
FACEBOOK_PAGE_ID=your_page_id
FACEBOOK_PAGE_ACCESS_TOKEN=your_page_access_token
```

Optional (for token generation):
```
FB_APP_ID=your_app_id
FB_APP_SECRET=your_app_secret
FB_SHORT_USER_TOKEN=your_short_lived_token
```

## Mock Mode

When Facebook credentials are not configured, the module runs in mock mode:
- Posts are created in database but not sent to Facebook
- Mock analytics data is returned
- All features work for testing purposes
- Posts are marked with `mock: true` flag

## Frontend Usage

1. Navigate to movie detail page
2. Click "Facebook Campaign" button (only visible for current movies)
3. Use tabs to:
   - **Create Post**: Generate and customize posts
   - **Campaign Schedule**: View 30-day campaign plan
   - **My Posts**: Track all created/scheduled posts

## Campaign Types Explained

### Teaser (30 days before release)
- Mysterious announcement
- Builds anticipation
- Minimal details revealed

### Cast Reveal (25 days before)
- Announce star cast
- Character details
- Actor highlights

### Trailer (20 days before)
- Official trailer release
- Video link
- Engagement prompts

### Countdown (15, 10, 7, 3, 1 days before)
- Time-based urgency
- Release date reminders
- Booking prompts

### Release Day
- Launch announcement
- Theater information
- Ticket booking links

## Best Practices

1. **Start Early**: Begin campaign 30 days before release
2. **Consistent Posting**: Follow the generated schedule
3. **Visual Content**: Always include images or videos
4. **Engagement**: Use hashtags and call-to-action
5. **Track Analytics**: Monitor post performance
6. **Adjust Strategy**: Modify based on engagement data

## Technical Notes

- Posts are stored in `facebook_posts` collection
- Scheduled posts can be deleted before posting
- Mock mode allows testing without Facebook API
- All dates are in UTC timezone
- Images must be publicly accessible URLs
