# Film Intel API Documentation

## Authentication Endpoints

### Register New Producer
```
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "producer@example.com",
  "username": "producer123",
  "password": "securepassword",
  "full_name": "John Producer"
}
```

**Response:**
```json
{
  "id": "user_id",
  "email": "producer@example.com",
  "username": "producer123",
  "full_name": "John Producer",
  "is_active": true
}
```

### Login
```
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "producer@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User
```
GET /api/v1/auth/me
Authorization: Bearer <token>
```

## Movie/Project Endpoints

### Create New Movie Project
```
POST /api/v1/movies/
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "My New Film",
  "director": "Director Name",
  "genre": "Drama",
  "budget": 25000000,
  "budget_currency": "INR",
  "release_date": "2024-12-15T00:00:00",
  "language": "Hindi",
  "themes": "Family, Drama, Social",
  "region": "Pan-India",
  "cast": [
    {
      "name": "Actor Name",
      "role": "Lead",
      "star_power": 85.0
    }
  ],
  "status": "pre-production"
}
```

**Response:**
```json
{
  "id": "movie_id",
  "title": "My New Film",
  "director": "Director Name",
  "genre": "Drama",
  "budget": 25000000,
  "budget_currency": "INR",
  "release_date": "2024-12-15T00:00:00",
  "language": "Hindi",
  "themes": "Family, Drama, Social",
  "region": "Pan-India",
  "cast": [...],
  "producer_id": "user_id",
  "status": "pre-production",
  "cast_score": 85.0,
  "historic_score": 72.5,
  "public_pulse_score": 68.0,
  "hws_score": null,
  "created_at": "2024-01-15T10:30:00",
  "updated_at": "2024-01-15T10:30:00"
}
```

### Get My Movies
```
GET /api/v1/movies/
Authorization: Bearer <token>
```

Returns all movies created by the authenticated producer.

### Get All Movies (For Competitor Analysis)
```
GET /api/v1/movies/all
Authorization: Bearer <token>
```

Returns all movies with status "awaiting-release" or "released" from all producers.

### Get Single Movie
```
GET /api/v1/movies/{movie_id}
Authorization: Bearer <token>
```

### Update Movie
```
PUT /api/v1/movies/{movie_id}
Authorization: Bearer <token>
```

**Request Body:** (all fields optional)
```json
{
  "title": "Updated Title",
  "release_date": "2024-12-20T00:00:00",
  "status": "awaiting-release"
}
```

### Delete Movie
```
DELETE /api/v1/movies/{movie_id}
Authorization: Bearer <token>
```

## Competitor Analysis Endpoints

### Analyze Competitor
```
POST /api/v1/movies/{movie_id}/analyze-competitor
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "competitor_movie_id": "competitor_movie_id"
}
```

**Response:**
```json
{
  "movie_id": "your_movie_id",
  "competitor_movie_id": "competitor_movie_id",
  "your_movie_title": "My New Film",
  "competitor_movie_title": "Competitor Film",
  "your_cast_score": 85.0,
  "competitor_cast_score": 78.0,
  "your_historic_score": 72.5,
  "competitor_historic_score": 80.0,
  "your_pulse_score": 68.0,
  "competitor_pulse_score": 65.0,
  "overall_strength": "stronger",
  "recommendation": "Your film is stronger by 3.5 points. Capitalize on this advantage with aggressive marketing.",
  "release_date_conflict": true,
  "days_apart": 7
}
```

### Get All Competitors for a Movie
```
GET /api/v1/movies/{movie_id}/competitors
Authorization: Bearer <token>
```

Returns list of all competitor analyses for the specified movie.

## Score Calculation

### Cast Score
- Calculated based on star power of cast members
- Range: 0-100
- Formula: Average of all cast members' star power

### Historic Score
- Based on director's past performance and genre trends
- Range: 0-100
- Factors: Director reputation, genre market performance

### Public Pulse Score
- Sentiment analysis from social media and public interest
- Range: 0-100
- Factors: Theme relevance, trending topics, social buzz

### Overall Strength Comparison
- Weighted average: Cast (40%) + Historic (30%) + Pulse (30%)
- Results: "stronger", "weaker", or "equal"
- Threshold: ±5 points for "equal"

## Release Date Conflict Detection

Movies are considered in conflict if:
- Release dates are within 14 days of each other
- Both are targeting similar markets/regions
- Genre overlap exists

## Authentication

All movie and competitor endpoints require JWT authentication:

```
Authorization: Bearer <your_access_token>
```

Get the access token from the `/auth/login` endpoint.

## Status Codes

- 200: Success
- 201: Created
- 204: No Content (successful deletion)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Internal Server Error


## Release Strategy Endpoints

### Analyze Date Range with Competitors
```
POST /api/v1/release-strategy/analyze-date-range
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "movie_id": "your_movie_id",
  "target_release_date": "2024-12-15T00:00:00",
  "days_before": 30,
  "days_after": 30
}
```

**Response:**
```json
{
  "movie_id": "your_movie_id",
  "your_movie_title": "My Film",
  "your_movie_category": "medium",
  "target_release_date": "2024-12-15T00:00:00",
  "date_range_start": "2024-11-15T00:00:00",
  "date_range_end": "2025-01-14T00:00:00",
  "total_competitors": 8,
  "competitors": [
    {
      "movie_id": "comp_id",
      "title": "Competitor Film",
      "director": "Director Name",
      "genre": "Drama",
      "budget": 50000000,
      "release_date": "2024-12-10T00:00:00",
      "category": "big",
      "cast_score": 85.0,
      "historic_score": 78.0,
      "public_pulse_score": 72.0,
      "days_from_your_release": 5,
      "threat_level": "high",
      "language": "Hindi",
      "region": "Pan-India"
    }
  ],
  "big_movies_count": 2,
  "medium_movies_count": 3,
  "small_movies_count": 3,
  "high_threat_count": 2,
  "recommendation": "High risk window. 2 high-threat competitors detected. Strongly consider alternative dates.",
  "optimal_release_windows": [
    {
      "start_date": "2024-12-20T00:00:00",
      "end_date": "2024-12-27T00:00:00",
      "reason": "Clear window with no direct competition"
    }
  ],
  "risk_assessment": "HIGH - Multiple direct competitors"
}
```

### Generate PR Strategy (AI-Powered)
```
POST /api/v1/release-strategy/pr-strategy
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "movie_id": "your_movie_id",
  "competitor_movie_ids": ["comp_id_1", "comp_id_2"],
  "focus_areas": ["social_media", "press", "influencer", "events"]
}
```

**Response:**
```json
{
  "movie_id": "your_movie_id",
  "movie_title": "My Film",
  "movie_category": "medium",
  "pr_strategy": "Position as authentic regional cinema with universal themes...",
  "key_differentiators": [
    "Authentic storytelling with regional flavor",
    "Strong director reputation in indie circuit",
    "Unique thematic approach to family dynamics"
  ],
  "target_audience_approach": {
    "primary": "Urban millennials interested in meaningful cinema",
    "secondary": "Festival circuit audience and critics"
  },
  "media_channels": [
    {
      "channel": "Social Media",
      "tactics": "Behind-the-scenes content, director interviews",
      "budget_percent": 35
    }
  ],
  "timeline": [
    {
      "phase": "Pre-release (8-12 weeks)",
      "activities": "Festival submissions, teaser release"
    }
  ],
  "budget_allocation": {
    "digital_marketing": 40,
    "traditional_media": 20,
    "events_screenings": 25
  },
  "risk_mitigation": [
    "Build strong critic relationships early",
    "Create viral-worthy content pieces"
  ],
  "success_metrics": [
    "Social media engagement rate > 5%",
    "Press coverage in 10+ major outlets"
  ]
}
```

### AI Release Date Decision
```
POST /api/v1/release-strategy/release-date-decision
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "movie_id": "your_movie_id",
  "target_release_date": "2024-12-15T00:00:00",
  "days_before": 45,
  "days_after": 45
}
```

**Response:**
```json
{
  "movie_id": "your_movie_id",
  "current_target_date": "2024-12-15T00:00:00",
  "recommended_date": "2024-12-20T00:00:00",
  "confidence_score": 78,
  "reasoning": "Current date has moderate competition. Moving 5 days later provides clearer window...",
  "alternative_dates": [
    {
      "date": "2024-12-13",
      "pros": "Earlier window, less competition",
      "cons": "Less time for marketing buildup"
    }
  ],
  "competitive_analysis": "Two big movies within 10 days create crowded marketplace...",
  "market_conditions": "December is strong for family dramas. Holiday season provides extended viewing window.",
  "action_items": [
    "Confirm new date within 48 hours",
    "Adjust marketing timeline accordingly"
  ]
}
```

## Movie Categorization

Movies are automatically categorized as:

- **Big Movie**: Budget ≥ ₹5 Cr AND Cast Score ≥ 75
- **Medium Movie**: Budget ≥ ₹1.5 Cr OR Cast Score ≥ 70
- **Small Movie**: Budget < ₹1.5 Cr AND Cast Score < 70

## Threat Level Calculation

Threat levels are calculated based on:
- Date proximity (within 7 days = high threat)
- Genre match
- Language/region overlap
- Movie category comparison
- Competitive scores

Levels: **high**, **medium**, **low**
