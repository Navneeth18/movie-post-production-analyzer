# 🎯 Public Pulse Module - Complete Documentation

## Overview

The Public Pulse module is a separate feature that analyzes YouTube trailer data to calculate audience sentiment and track it over time. It provides real-time insights into how the public is responding to your movie trailer.

## Features

### ✅ YouTube Trailer Integration
- Add YouTube trailer URL to any movie
- Automatic video ID extraction
- Embedded video player in analytics page

### ✅ Sentiment Analysis
- Analyzes top 10 comments for sentiment
- Calculates like/dislike ratio
- Measures engagement rate (likes+dislikes/views)
- Overall pulse score (0-100)

### ✅ Time-Series Tracking
- Historical data storage
- Day-by-day pulse tracking
- Visual graph representation
- Trend analysis

### ✅ Real-Time Metrics
- Current pulse score
- Total likes
- Total views
- Engagement rate percentage
- Sentiment classification (Positive/Neutral/Negative)

## Backend API Endpoints

### 1. Add YouTube Trailer
```
POST /api/v1/public-pulse/{movie_id}/add-trailer
```

**Request Body:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

**Response:**
```json
{
  "message": "Trailer added successfully",
  "video_id": "VIDEO_ID",
  "pulse_score": 75.5,
  "youtube_data": {
    "likes": 15000,
    "dislikes": 500,
    "views": 500000,
    "comments": [...]
  }
}
```

### 2. Refresh Public Pulse
```
POST /api/v1/public-pulse/{movie_id}/refresh-pulse
```

Fetches latest YouTube data and recalculates pulse score.

### 3. Get Current Pulse
```
GET /api/v1/public-pulse/{movie_id}/current
```

**Response:**
```json
{
  "movie_id": "...",
  "movie_title": "Movie Title",
  "youtube_video_id": "VIDEO_ID",
  "current_pulse_score": 75.5,
  "likes": 15000,
  "dislikes": 500,
  "views": 500000,
  "engagement_rate": 3.1,
  "sentiment": "Positive",
  "last_updated": "2026-02-20T..."
}
```

### 4. Get Pulse History
```
GET /api/v1/public-pulse/{movie_id}/history
```

Returns array of historical pulse data for graphing.

### 5. Remove Trailer
```
DELETE /api/v1/public-pulse/{movie_id}/trailer
```

## Pulse Score Calculation

The pulse score (0-100) is calculated using:

### 1. Like/Dislike Ratio (30% weight)
```
like_ratio = likes / (likes + dislikes)
like_score = like_ratio * 100
contribution = (like_score - 50) * 0.3
```

### 2. Engagement Rate (20% weight)
```
engagement_rate = (likes + dislikes) / views
engagement_score = min(engagement_rate / 0.05 * 100, 100)
contribution = (engagement_score - 50) * 0.2
```

### 3. Comment Sentiment (50% weight)
```
Analyzes top 10 comments for positive/negative keywords
sentiment_score = 50 + (positive_ratio * 50) - (negative_ratio * 50)
contribution = (sentiment_score - 50) * 0.5
```

**Final Score:**
```
pulse_score = 50 + sum(all contributions)
clamped to [0, 100]
```

## Sentiment Classification

- **Positive**: Pulse score >= 70
- **Neutral**: Pulse score 50-69
- **Negative**: Pulse score < 50

## Frontend Pages

### Public Pulse Analytics Page
**Route:** `/movies/:id/public-pulse`

**Features:**
- Add YouTube trailer form
- Current pulse metrics dashboard
- Embedded YouTube video
- Line graph showing pulse over time
- Historical data table
- Refresh button to update data

**Components:**
- Pulse score card (blue)
- Likes card (green)
- Views card (purple)
- Engagement rate card (orange)
- Chart.js line graph
- Data table

## YouTube API Integration

### Setup
1. Get YouTube Data API v3 key from Google Cloud Console
2. Add to `.env`:
```env
YOUTUBE_API_KEY=your_api_key_here
```

### API Calls
The service fetches:
- Video statistics (likes, views, comment count)
- Top 10 comments (sorted by relevance)

### Fallback
If no API key is provided, mock data is used for testing.

## Database Schema

### Movies Collection
```javascript
{
  youtube_video_id: String,
  youtube_url: String,
  public_pulse_score: Float
}
```

### Pulse History Collection
```javascript
{
  movie_id: String,
  pulse_score: Float,
  likes: Integer,
  dislikes: Integer,
  views: Integer,
  comments_analyzed: Integer,
  recorded_at: DateTime
}
```

## Usage Workflow

### 1. Add Trailer
1. Navigate to movie detail page
2. Click "Public Pulse Analytics"
3. Enter YouTube trailer URL
4. Click "Add Trailer"
5. System fetches data and calculates initial pulse

### 2. Track Over Time
1. Click "Refresh Data" button periodically
2. System fetches latest YouTube stats
3. New data point added to history
4. Graph updates automatically

### 3. Analyze Trends
1. View line graph for trends
2. Check if pulse is increasing/decreasing
3. Correlate with marketing campaigns
4. Adjust strategy based on sentiment

## Movie Cards Update

### Removed from Cards:
- ❌ Historic Score
- ❌ Public Pulse Score

### Shown in Cards:
- ✅ Cast Score
- ✅ HWS Score (for historical movies)

### Access Public Pulse:
- Click on movie → "Public Pulse Analytics" button

## Installation

### Backend
```bash
cd backend
pip install google-api-python-client
```

### Frontend
```bash
cd frontend_new
npm install chart.js react-chartjs-2
```

## Testing

### 1. Test with Mock Data
No API key needed - uses mock data automatically.

### 2. Test with Real YouTube Data
1. Get YouTube API key
2. Add to `.env`
3. Use real trailer URL
4. Verify data fetching

### 3. Test Refresh
1. Add trailer
2. Wait a few minutes
3. Click "Refresh Data"
4. Verify new data point in graph

## Example YouTube URLs

Supported formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Sentiment Keywords

### Positive Keywords
amazing, awesome, great, excellent, fantastic, wonderful, love, best, perfect, brilliant, outstanding, superb, excited, waiting, can't wait, masterpiece, blockbuster, goosebumps, fire, 🔥, ❤️, 👏, 💯

### Negative Keywords
bad, worst, terrible, awful, horrible, disappointing, waste, boring, poor, flop, disaster, pathetic, overrated, cringe, skip, avoid, 👎, 😴

## Future Enhancements

### Planned Features
1. **Transformer-based Sentiment Analysis**
   - Use distilbert-base-uncased-finetuned-sst-2-english
   - More accurate sentiment detection
   - Multi-language support

2. **Automated Tracking**
   - Scheduled daily pulse updates
   - Email notifications on significant changes
   - Alerts for negative sentiment spikes

3. **Comparative Analysis**
   - Compare pulse with competitor trailers
   - Industry benchmarks
   - Genre-specific averages

4. **Advanced Metrics**
   - Comment velocity (comments per hour)
   - Share rate
   - Subscriber conversion rate
   - Geographic distribution

5. **AI Insights**
   - Automatic trend detection
   - Predictive analytics
   - Recommendation engine

## Troubleshooting

### No Data Showing
- Verify YouTube URL is correct
- Check if API key is valid
- Ensure video is public
- Check browser console for errors

### Graph Not Updating
- Click "Refresh Data" button
- Check if new data point was added
- Verify pulse_history collection in MongoDB

### API Rate Limits
- YouTube API has daily quota
- Implement caching
- Use refresh sparingly
- Consider upgrading API quota

---

**Public Pulse module is now fully functional!** 🎬📊
