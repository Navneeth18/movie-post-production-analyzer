# Feature Restrictions for Historical vs Current Movies

## Overview
Historical movies (tag="past") are restricted from using certain features that are only relevant for current/upcoming movies.

## Restricted Features for Historical Movies

### 1. Public Pulse (YouTube Sentiment Analysis)
- ❌ Cannot add YouTube trailer
- ❌ Cannot refresh pulse data
- ❌ Cannot view current pulse
- ❌ Cannot view pulse history

**Reason**: Historical movies have already been released. Public pulse is for tracking pre-release and post-release sentiment for current movies.

**Endpoints Restricted**:
- `POST /api/v1/public-pulse/{movie_id}/add-trailer`
- `POST /api/v1/public-pulse/{movie_id}/refresh-pulse`
- `GET /api/v1/public-pulse/{movie_id}/current`
- `GET /api/v1/public-pulse/{movie_id}/history`

### 2. Competitor Analysis
- ❌ Cannot analyze competitors
- ❌ Cannot view competitor comparisons

**Reason**: Competitor analysis is for planning release strategy. Historical movies have already been released.

**Endpoints Restricted**:
- `POST /api/v1/movies/{movie_id}/analyze-competitor`
- `GET /api/v1/movies/{movie_id}/competitors`

### 3. Release Strategy
- ❌ Cannot analyze release date ranges
- ❌ Cannot generate PR strategy
- ❌ Cannot get release date decisions

**Reason**: Release strategy planning is only relevant for upcoming movies, not movies that have already been released.

**Endpoints Restricted**:
- `POST /api/v1/release-strategy/analyze-date-range`
- `POST /api/v1/release-strategy/pr-strategy`
- `POST /api/v1/release-strategy/release-date-decision`

## Available Features for Historical Movies

### ✅ View Movie Details
- Can view all movie information
- Can see HWS score and breakdown
- Can see cast score
- Can view budget, revenue, IMDb rating

### ✅ HWS Calculation
- HWS is automatically calculated for historical movies
- Uses director, hero, heroine from database
- Estimates popularity score from budget/revenue ratio

## Available Features for Current Movies

### ✅ All Historical Movie Features PLUS:
- Public Pulse tracking
- Competitor analysis
- Release strategy planning
- PR strategy generation
- Movie editing and updates

## Implementation Details

### How Restrictions Work
1. Each restricted endpoint checks `movie.get("tag")`
2. If tag is "past", returns HTTP 400 with error message
3. Error message: "Feature is only available for current movies"

### Movie Tag System
- **"current"**: Movies in production, post-production, or awaiting release
- **"past"**: Movies that have been released (status="released")

### Automatic Tag Updates
- When a movie's status changes to "released", tag automatically updates to "past"
- This happens in the movie update endpoint

## Testing

Run the test scripts to verify restrictions:

```bash
# Test movie update functionality
python test_movie_update.py

# Test historical movie restrictions
python test_historical_restrictions.py
```

## Error Messages

When a historical movie tries to use a restricted feature:

```json
{
  "detail": "Public pulse is only available for current movies, not historical movies"
}
```

```json
{
  "detail": "Competitor analysis is only available for current movies"
}
```

```json
{
  "detail": "Release strategy analysis is only available for current movies"
}
```

## Frontend Integration

The frontend should:
1. Check movie tag before showing feature buttons
2. Hide/disable public pulse, competitors, and strategy buttons for historical movies
3. Show appropriate message if user tries to access restricted features
4. Only show these features for current movies (tag="current")

Example frontend check:
```javascript
const isCurrentMovie = movie.tag === 'current' || movie.source === 'current';

// Only show these buttons for current movies
{isCurrentMovie && (
  <>
    <button onClick={openPublicPulse}>Public Pulse</button>
    <button onClick={openCompetitors}>Competitors</button>
    <button onClick={openStrategy}>Release Strategy</button>
  </>
)}
```
