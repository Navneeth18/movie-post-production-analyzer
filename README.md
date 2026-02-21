# Film Intel Platform - Complete Documentation

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Software Requirements Specification (SRS)](#software-requirements-specification)
4. [Technical Stack](#technical-stack)
5. [Module Documentation](#module-documentation)
6. [API Documentation](#api-documentation)
7. [Database Schema](#database-schema)
8. [Deployment Guide](#deployment-guide)

---

## Executive Summary

**Film Intel Platform** is an AI-powered film production intelligence system designed for Telugu cinema producers. It provides data-driven insights for movie production decisions, competitive analysis, marketing strategy, and release planning.

### Key Features
- **HWS Score Calculation**: Hit/Washout/Semi-hit prediction algorithm
- **Public Pulse Monitoring**: Real-time sentiment analysis from YouTube
- **Release Strategy Analysis**: Competitive landscape assessment
- **Budget Planning**: AI-optimized marketing budget allocation
- **Facebook Campaign Automation**: AI-generated posters and automated posting
- **Data Analytics Dashboard**: Historical performance insights
- **Competitor Analysis**: Head-to-head movie comparison

### Target Users
- Film Producers
- Production Houses
- Marketing Teams
- Distribution Companies

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  React 18 + Vite + TailwindCSS + Zustand + React Router   │
└────────────────────┬────────────────────────────────────────┘
                     │ REST API (HTTP/JSON)
┌────────────────────▼────────────────────────────────────────┐
│                    Backend Layer                            │
│         FastAPI + Python 3.11 + Pydantic                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints (11 modules)                          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Business Logic Services (12 services)               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──────┐ ┌──▼──────┐ ┌──▼────────────┐
│   MongoDB    │ │ ChromaDB│ │ External APIs │
│  (Primary)   │ │ (Vector)│ │ - YouTube     │
│              │ │         │ │ - Ollama      │
│              │ │         │ │ - Pollinations|
│              | |         | | - FaceBook    |
└──────────────┘ └─────────┘ └───────────────┘
```


### Architecture Layers

#### 1. Presentation Layer (Frontend)
- **Technology**: React 18 with Vite build tool
- **State Management**: Zustand for global state
- **Routing**: React Router v6 for SPA navigation
- **Styling**: TailwindCSS for responsive UI
- **Charts**: Chart.js + react-chartjs-2 for data visualization
- **HTTP Client**: Axios for API communication

#### 2. Application Layer (Backend)
- **Framework**: FastAPI (async Python web framework)
- **Authentication**: JWT tokens with passlib + bcrypt
- **Validation**: Pydantic models for request/response validation
- **CORS**: Configured for localhost development

#### 3. Business Logic Layer (Services)
- **HWS Service**: Hit prediction algorithm
- **Release Strategy Service**: Competitive analysis
- **DeepSeek Service**: AI-powered recommendations
- **Facebook Service**: Campaign automation
- **YouTube Sentiment Service**: Public pulse monitoring
- **Analytics Service**: Historical data analysis
- **Scraper Service**: Web data collection

#### 4. Data Layer
- **Primary Database**: MongoDB (document store)
- **Vector Database**: ChromaDB (for semantic search)
- **Collections**: users, movies, pr_strategies, sentiment_history

#### 5. External Integration Layer
- **YouTube Data API v3**: Video sentiment analysis
- **Ollama**: Local LLM (DeepSeek R1:7b)
- **Pollinations AI**: Image generation for posters
- **Facebook Graph API**: Automated posting

---

## Software Requirements Specification (SRS)

### 1. Functional Requirements

#### FR1: User Management
- **FR1.1**: User registration with email, username, password
- **FR1.2**: User authentication with JWT tokens
- **FR1.3**: Session management (24-hour token expiry)
- **FR1.4**: Role-based access (Producer role)

#### FR2: Movie Management
- **FR2.1**: Create movie with title, director, cast, budget, genres, languages
- **FR2.2**: Edit movie details
- **FR2.3**: View movie list (producer's movies only)
- **FR2.4**: View detailed movie information
- **FR2.5**: Delete movie
- **FR2.6**: Tag movies as "current" or "past"

#### FR3: HWS Score Calculation
- **FR3.1**: Calculate HWS score based on 7 weighted factors:
  - Director reputation (Wd = 0.20)
  - Historical performance (Wh = 0.15)
  - Sentiment analysis (Ws = 0.15)
  - Public pulse (Wp = 0.15)
  - Genre popularity (Wg = 0.10)
  - Budget allocation (Wb = 0.15)
  - Release timing (Wt = 0.10)
- **FR3.2**: Categorize movie as Big/Medium/Small based on HWS
- **FR3.3**: Provide market action recommendation (Go/Caution/Stop)
- **FR3.4**: Display HWS breakdown with component scores


#### FR4: Public Pulse Monitoring
- **FR4.1**: Connect YouTube video to movie
- **FR4.2**: Fetch video statistics (views, likes, comments)
- **FR4.3**: Analyze comment sentiment (positive/negative/neutral)
- **FR4.4**: Calculate public pulse score (0-100)
- **FR4.5**: Track sentiment history over time
- **FR4.6**: Display sentiment trends with charts
- **FR4.7**: Provide AI-powered insights on public perception

#### FR5: Release Strategy Analysis
- **FR5.1**: Analyze competitors in ±30 day window
- **FR5.2**: Categorize competitors by size (big/medium/small)
- **FR5.3**: Calculate threat level (high/medium/low)
- **FR5.4**: Compare cast, historic, and pulse scores
- **FR5.5**: Identify optimal release windows
- **FR5.6**: Generate risk assessment
- **FR5.7**: Provide release date recommendations
- **FR5.8**: AI-powered PR strategy generation

#### FR6: Budget Planning
- **FR6.1**: Allocate budget across 6 marketing channels:
  - Digital Marketing (Social Media, YouTube, OTT)
  - Traditional Media (TV, Print, Radio)
  - Influencer Marketing
  - Events & Promotions
  - PR & Media Relations
  - Contingency Fund
- **FR6.2**: Calculate ROI for each channel
- **FR6.3**: Set campaign timeline (4-16 weeks)
- **FR6.4**: Provide genre-specific optimal presets
- **FR6.5**: AI-optimized budget recommendations (DeepSeek R1)
- **FR6.6**: Real-time budget validation
- **FR6.7**: Auto-save budget plans

#### FR7: Facebook Campaign Automation
- **FR7.1**: Generate AI posters using Pollinations AI
- **FR7.2**: Customize poster with movie details
- **FR7.3**: Preview generated posters
- **FR7.4**: Schedule posts to Facebook Page
- **FR7.5**: Post immediately or schedule for later
- **FR7.6**: Track campaign history
- **FR7.7**: Manage Facebook Page access tokens

#### FR8: Data Analytics Dashboard
- **FR8.1**: Grade-Performance Correlation (Bar Chart)
  - IMDB ratings by director grade
  - Outlier detection
- **FR8.2**: Genre Popularity Timeline (Area Chart)
  - Quarterly trends
  - Multi-genre tracking
- **FR8.3**: Talent Value Matrix (Bubble Chart)
  - Hero performance (IMDB vs Popularity)
  - Bubble size = movie count
- **FR8.4**: Demographic Heatmap (Matrix)
  - Genre-Age group correlation
  - Average popularity scores

#### FR9: Competitor Analysis
- **FR9.1**: Head-to-head movie comparison
- **FR9.2**: Compare cast, historic, pulse scores
- **FR9.3**: Identify release date conflicts
- **FR9.4**: Calculate days apart
- **FR9.5**: Overall strength assessment
- **FR9.6**: Strategic recommendations


### 2. Non-Functional Requirements

#### NFR1: Performance
- **NFR1.1**: API response time < 2 seconds (95th percentile)
- **NFR1.2**: AI operations (DeepSeek) timeout: 180 seconds
- **NFR1.3**: Support 100 concurrent users
- **NFR1.4**: Database query optimization with indexes
- **NFR1.5**: Frontend bundle size < 500KB (gzipped)

#### NFR2: Security
- **NFR2.1**: Password hashing with bcrypt (cost factor 12)
- **NFR2.2**: JWT token-based authentication
- **NFR2.3**: HTTPS for production deployment
- **NFR2.4**: API key protection for external services
- **NFR2.5**: CORS configuration for allowed origins
- **NFR2.6**: Input validation with Pydantic
- **NFR2.7**: SQL injection prevention (NoSQL)

#### NFR3: Scalability
- **NFR3.1**: Horizontal scaling with load balancer
- **NFR3.2**: MongoDB replica set for high availability
- **NFR3.3**: Async operations for I/O-bound tasks
- **NFR3.4**: Caching strategy for frequently accessed data
- **NFR3.5**: CDN for static assets

#### NFR4: Reliability
- **NFR4.1**: 99.5% uptime SLA
- **NFR4.2**: Automated database backups (daily)
- **NFR4.3**: Error logging and monitoring
- **NFR4.4**: Graceful degradation (fallback responses)
- **NFR4.5**: Health check endpoints

#### NFR5: Usability
- **NFR5.1**: Responsive design (mobile, tablet, desktop)
- **NFR5.2**: Intuitive navigation with breadcrumbs
- **NFR5.3**: Loading states for async operations
- **NFR5.4**: Toast notifications for user feedback
- **NFR5.5**: Form validation with error messages
- **NFR5.6**: Dark mode UI theme

#### NFR6: Maintainability
- **NFR6.1**: Modular architecture (separation of concerns)
- **NFR6.2**: Code documentation with docstrings
- **NFR6.3**: RESTful API design
- **NFR6.4**: Version control with Git
- **NFR6.5**: Environment-based configuration
- **NFR6.6**: Logging with structured format

---

## Technical Stack

### Backend Stack
```yaml
Language: Python 3.11+
Framework: FastAPI 0.109.0
Server: Uvicorn (ASGI)
Database: MongoDB 4.6+ (Motor async driver)
Vector DB: ChromaDB
Authentication: JWT (python-jose)
Password Hashing: bcrypt + passlib
Validation: Pydantic 2.5+
HTTP Client: httpx
Date Handling: python-dateutil
External APIs:
  - google-api-python-client (YouTube)
  - Ollama (Local LLM)
  - Pollinations AI (Image generation)
```

### Frontend Stack
```yaml
Language: JavaScript (ES6+)
Framework: React 18.2
Build Tool: Vite 5.1
Routing: React Router DOM 6.22
State Management: Zustand 4.5
Styling: TailwindCSS 3.4 + PostCSS + Autoprefixer
HTTP Client: Axios 1.6
Charts: Chart.js 4.5 + react-chartjs-2 5.3
Icons: Lucide React 0.468
Notifications: React Hot Toast 2.4
Date Handling: date-fns 3.3
```


### Development Tools
```yaml
Version Control: Git
Package Managers:
  - Backend: pip
  - Frontend: npm
Environment: .env files
Code Quality:
  - Backend: Python type hints
  - Frontend: ESLint
API Testing: Postman / Thunder Client
```

---

## Module Documentation

### Backend Modules

#### 1. Authentication Module (`/api/v1/auth`)
**Purpose**: User registration, login, and session management

**Endpoints**:
- `POST /register` - Create new user account
- `POST /login` - Authenticate and get JWT token
- `GET /me` - Get current user profile

**Models**:
- `User`: email, username, full_name, hashed_password, is_active, created_at
- `UserInDB`: User + id

**Security**:
- Password hashing with bcrypt
- JWT tokens (24-hour expiry)
- Token validation middleware

---

#### 2. Movies Module (`/api/v1/movies`)
**Purpose**: CRUD operations for movie management

**Endpoints**:
- `GET /` - List all movies for current producer
- `POST /` - Create new movie
- `GET /{id}` - Get movie details
- `PUT /{id}` - Update movie
- `DELETE /{id}` - Delete movie
- `POST /{id}/calculate-hws` - Calculate HWS score

**Models**:
- `Movie`: title, director, genres[], budget, release_date, languages[], region, cast[], status, tag
- `CastMember`: name, role, star_power
- `MovieResponse`: Movie + id + scores + category

**Business Logic**:
- HWS calculation with 7 weighted factors
- Movie categorization (Big/Medium/Small)
- Market action recommendation

---

#### 3. Public Pulse Module (`/api/v1/public-pulse`)
**Purpose**: YouTube sentiment analysis and public perception tracking

**Endpoints**:
- `POST /{movie_id}/connect-video` - Link YouTube video
- `GET /{movie_id}/sentiment` - Get current sentiment
- `GET /{movie_id}/history` - Get sentiment history
- `POST /{movie_id}/refresh` - Refresh sentiment data

**External APIs**:
- YouTube Data API v3 (video stats, comments)

**Algorithm**:
```python
pulse_score = (
    (likes / (likes + dislikes)) * 40 +
    (positive_comments / total_comments) * 40 +
    (views / expected_views) * 20
)
```

**Features**:
- Real-time comment sentiment analysis
- Historical tracking with timestamps
- Trend visualization
- AI-powered insights


#### 4. Release Strategy Module (`/api/v1/release-strategy`)
**Purpose**: Competitive analysis and release date optimization

**Endpoints**:
- `POST /analyze-date-range` - Analyze competitors in date range
- `POST /pr-strategy` - Generate AI PR strategy
- `POST /release-date-decision` - Get AI release date recommendation

**Algorithm - Threat Level Calculation**:
```python
threat_score = 0
if days_diff <= 7: threat_score += 3
if genre_match: threat_score += 2
if language_match: threat_score += 2
if region_overlap: threat_score += 1
if competitor_bigger: threat_score += 2
if competitor_higher_scores: threat_score += 2

if threat_score >= 7: return "high"
elif threat_score >= 4: return "medium"
else: return "low"
```

**Features**:
- ±30 day competitor window analysis
- Multi-factor threat assessment
- Optimal release window identification
- Risk assessment (HIGH/MEDIUM/LOW)
- AI-powered recommendations (DeepSeek R1)

---

#### 5. Budget Planning Module (`/api/v1/budget`)
**Purpose**: Marketing budget allocation and optimization

**Endpoints**:
- `POST /calculate` - Calculate budget allocation
- `POST /optimize` - AI-optimized recommendations
- `GET /presets/{genre}` - Get genre-specific presets

**Channels** (6):
1. Digital Marketing (30-50%)
2. Traditional Media (15-30%)
3. Influencer Marketing (10-20%)
4. Events & Promotions (10-20%)
5. PR & Media Relations (5-15%)
6. Contingency Fund (5-10%)

**ROI Calculation**:
```python
roi = {
    'digital': allocation * 2.5,
    'traditional': allocation * 1.8,
    'influencer': allocation * 2.2,
    'events': allocation * 1.5,
    'pr': allocation * 2.0,
    'contingency': allocation * 1.0
}
```

**AI Integration**:
- DeepSeek R1:7b via Ollama
- 180-second timeout for chain-of-thought reasoning
- Fallback to rule-based recommendations

---

#### 6. Facebook Campaign Module (`/api/v1/facebook-campaign`)
**Purpose**: Automated poster generation and Facebook posting

**Endpoints**:
- `POST /generate-poster` - Generate AI poster
- `POST /post-to-facebook` - Post to Facebook Page
- `GET /campaigns` - List campaign history

**External APIs**:
- Pollinations AI: `https://gen.pollinations.ai/image`
- Facebook Graph API: Page posting

**Poster Generation**:
```python
prompt = f"{movie_title} - {genre} movie starring {cast}. 
          Cinematic poster, professional, high quality"
url = f"https://gen.pollinations.ai/image?prompt={prompt}&width=1080&height=1350"
```

**Features**:
- AI-generated movie posters
- Customizable prompts
- Immediate or scheduled posting
- Campaign tracking


#### 7. Data Analytics Module (`/api/v1/data-analytics`)
**Purpose**: Historical data analysis and insights

**Endpoints**:
- `GET /grade-performance` - Director grade vs IMDB ratings
- `GET /genre-timeline` - Genre popularity over time
- `GET /talent-matrix` - Hero performance matrix
- `GET /demographic-heatmap` - Genre-age group correlation

**Data Sources**:
- `bhanu_dataset.csv`: Movie details, ratings, popularity
- `bob-dataset.csv`: Talent grades (Director, Hero, Heroine)

**Visualizations**:
1. **Bar Chart**: IMDB ratings by director grade
2. **Area Chart**: Genre popularity quarterly trends
3. **Bubble Chart**: Hero IMDB vs Popularity (size = movie count)
4. **Heatmap**: Genre-age group average popularity

**Processing**:
- Pandas for data manipulation
- Multi-label genre/age group explosion
- Dataset merging by talent names
- Outlier detection

---

#### 8. Analytics Module (`/api/v1/analytics`)
**Purpose**: Legacy analytics endpoints

**Endpoints**:
- `GET /historical-movies` - Historical movie data
- `GET /artist-performance` - Artist performance metrics

---

#### 9. Calculator Module (`/api/v1/calculator`)
**Purpose**: HWS score calculation utilities

**Endpoints**:
- `POST /calculate-hws` - Calculate HWS score
- `GET /weights` - Get HWS weight configuration

---

#### 10. Marketing Module (`/api/v1/marketing`)
**Purpose**: Marketing strategy recommendations

**Endpoints**:
- `POST /strategy` - Generate marketing strategy
- `GET /channels` - List marketing channels

---

#### 11. Strategy Module (`/api/v1/strategy`)
**Purpose**: Overall strategic recommendations

**Endpoints**:
- `POST /analyze` - Comprehensive strategy analysis
- `GET /recommendations` - Get strategic recommendations

---

### Frontend Modules

#### 1. Authentication Pages
**Files**: `Login.jsx`, `Register.jsx`

**Features**:
- Form validation
- JWT token storage (localStorage)
- Auto-redirect on success
- Error handling with toast notifications

**State Management**:
```javascript
// Zustand store
const useAuthStore = create((set) => ({
  token: localStorage.getItem('token'),
  user: null,
  login: (token) => set({ token }),
  logout: () => set({ token: null, user: null })
}))
```


#### 2. Dashboard (`Dashboard.jsx`)
**Purpose**: Overview of producer's movies and quick actions

**Features**:
- Movie count statistics
- Recent movies list
- Quick navigation to key features
- Welcome message

---

#### 3. Movies Management
**Files**: `Movies.jsx`, `CreateMovie.jsx`, `EditMovie.jsx`, `MovieDetail.jsx`

**Movies List**:
- Grid/List view toggle
- Filter by status (all/pre-production/production/post-production/awaiting-release)
- Search by title
- Quick actions (view, edit, delete)

**Create/Edit Movie**:
- Multi-step form
- Genre multi-select
- Language multi-select
- Cast management (add/remove)
- Date picker for release date
- Budget input with currency
- Form validation

**Movie Detail**:
- Complete movie information
- HWS score display with breakdown
- Category badge (Big/Medium/Small)
- Market action indicator
- Navigation to features:
  - Public Pulse
  - Facebook Campaign
  - Budget Planning
  - Release Strategy
  - Competitor Analysis

---

#### 4. Public Pulse (`PublicPulse.jsx`)
**Purpose**: YouTube sentiment monitoring

**Features**:
- YouTube video connection form
- Current sentiment display:
  - Pulse score (0-100)
  - Sentiment breakdown (positive/negative/neutral)
  - Video statistics (views, likes, comments)
- Sentiment history chart (Line chart)
- Refresh button for latest data
- AI insights panel

**Chart Configuration**:
```javascript
{
  type: 'line',
  data: {
    labels: timestamps,
    datasets: [{
      label: 'Public Pulse Score',
      data: scores,
      borderColor: 'rgb(59, 130, 246)',
      tension: 0.4
    }]
  }
}
```

---

#### 5. Facebook Campaign (`FacebookCampaign.jsx`)
**Purpose**: Automated poster generation and posting

**Features**:
- Poster generation form:
  - Custom prompt input
  - Style selection
  - Preview before posting
- Generated poster display
- Post to Facebook:
  - Caption input
  - Schedule option
  - Immediate posting
- Campaign history table

**Workflow**:
1. Enter movie details
2. Generate AI poster
3. Preview poster
4. Customize caption
5. Post to Facebook
6. Track in history


#### 6. Budget Planning (`BudgetPlanning.jsx`)
**Purpose**: Marketing budget allocation and optimization

**Features**:
- Total budget input
- Timeline selection (4-16 weeks)
- 6 channel sliders with real-time validation
- ROI calculation per channel
- Total ROI display
- Genre-specific presets
- AI optimization button (DeepSeek R1)
- Markdown-formatted AI recommendations
- Auto-save functionality

**Validation**:
- Total allocation must equal 100%
- Warning if not balanced
- Min/max constraints per channel

**Markdown Formatter**:
```javascript
// Custom markdown parser for DeepSeek output
- Headers (H1-H4)
- Bold, Italic
- Bullet lists, Numbered lists
- Code blocks, Inline code
- Blockquotes
- Currency highlighting (₹)
```

---

#### 7. Data Analytics (`DataAnalytics.jsx`)
**Purpose**: Historical insights dashboard

**Features**:
- 4 interactive visualizations
- Dark mode theme
- Responsive layout
- Loading states
- Error handling

**Charts**:
1. **Grade-Performance Correlation**
   - Type: Bar Chart
   - X-axis: Director Grade (1, 2, 3)
   - Y-axis: Average IMDB Rating
   - Color: Gradient blue

2. **Genre Popularity Timeline**
   - Type: Area Chart
   - X-axis: Quarters (Q1 2023 - Q4 2024)
   - Y-axis: Total Popularity Score
   - Multiple datasets per genre

3. **Talent Value Matrix**
   - Type: Bubble Chart
   - X-axis: Average IMDB Rating
   - Y-axis: Average Popularity Score
   - Bubble size: Movie count
   - Color: Per hero

4. **Demographic Heatmap**
   - Type: Matrix Heatmap
   - Rows: Genres
   - Columns: Age Groups
   - Color intensity: Popularity score

---

#### 8. Competitor Analysis (`CompetitorAnalysis.jsx`)
**Purpose**: Head-to-head movie comparison

**Features**:
- Competitor selection dropdown
- Score comparison table:
  - Cast Score
  - Historic Score
  - Public Pulse Score
- Overall strength assessment
- Release date conflict detection
- Days apart calculation
- Strategic recommendations
- Visual score bars

---

#### 9. Release Date Analysis (`ReleaseDateAnalysis.jsx`)
**Purpose**: Release strategy and competitor landscape

**Features**:
- Date range selector (±30 days default)
- Competitor list with:
  - Movie details
  - Category badge
  - Threat level indicator
  - Days from release
  - Score comparison
- Statistics summary:
  - Total competitors
  - Big/Medium/Small count
  - High/Medium/Low threat count
- Risk assessment panel
- Optimal release windows
- AI recommendations
- Timeline visualization


#### 10. Layout Component (`Layout.jsx`)
**Purpose**: Main application shell with navigation

**Features**:
- Sidebar navigation
- User profile display
- Logout functionality
- Active route highlighting
- Responsive design
- Nested routing (Outlet)

**Navigation Items**:
- Dashboard
- My Movies
- Analytics
- Profile
- Logout

---

## API Documentation

### Base URL
```
Development: http://localhost:8000/api/v1
Production: https://your-domain.com/api/v1
```

### Authentication
All protected endpoints require JWT token in header:
```
Authorization: Bearer <token>
```

### Common Response Formats

**Success Response**:
```json
{
  "status": "success",
  "data": { ... },
  "message": "Operation successful"
}
```

**Error Response**:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### Endpoint Reference

#### Authentication Endpoints

**POST /auth/register**
```json
Request:
{
  "email": "producer@example.com",
  "username": "producer123",
  "full_name": "John Producer",
  "password": "SecurePass@123"
}

Response:
{
  "id": "507f1f77bcf86cd799439011",
  "email": "producer@example.com",
  "username": "producer123",
  "full_name": "John Producer",
  "is_active": true
}
```

**POST /auth/login**
```json
Request:
{
  "email": "producer@example.com",
  "password": "SecurePass@123"
}

Response:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**GET /auth/me**
```json
Response:
{
  "id": "507f1f77bcf86cd799439011",
  "email": "producer@example.com",
  "username": "producer123",
  "full_name": "John Producer",
  "is_active": true
}
```


#### Movie Endpoints

**POST /movies**
```json
Request:
{
  "title": "Action Hero",
  "director": "S. S. Rajamouli",
  "genres": ["Action", "Drama"],
  "budget": 150000000,
  "budget_currency": "INR",
  "release_date": "2026-03-15T00:00:00Z",
  "languages": ["Telugu", "Hindi"],
  "region": "Pan-India",
  "cast": [
    {
      "name": "Allu Arjun",
      "role": "Lead 1 (Hero)",
      "star_power": 95
    }
  ],
  "status": "pre-production"
}

Response:
{
  "id": "507f1f77bcf86cd799439012",
  "title": "Action Hero",
  ...
  "tag": "current",
  "created_at": "2024-02-21T10:30:00Z"
}
```

**GET /movies**
```json
Response:
[
  {
    "id": "507f1f77bcf86cd799439012",
    "title": "Action Hero",
    "director": "S. S. Rajamouli",
    "genres": ["Action", "Drama"],
    "budget": 150000000,
    "release_date": "2026-03-15T00:00:00Z",
    "status": "pre-production",
    "hws_score": 75.5,
    "category": "Big",
    "cast_score": 85,
    "historic_score": 78,
    "public_pulse_score": 72
  }
]
```

**POST /movies/{id}/calculate-hws**
```json
Request:
{
  "director_score": 85,
  "historical_score": 78,
  "sentiment_score": 72,
  "pulse_score": 75,
  "genre_score": 80,
  "budget_score": 70,
  "timing_score": 65
}

Response:
{
  "hws_score": 75.5,
  "category": "Big",
  "market_action": "Go",
  "breakdown": {
    "director": 17.0,
    "historical": 11.7,
    "sentiment": 10.8,
    "pulse": 11.25,
    "genre": 8.0,
    "budget": 10.5,
    "timing": 6.5
  }
}
```

#### Public Pulse Endpoints

**POST /public-pulse/{movie_id}/connect-video**
```json
Request:
{
  "youtube_video_id": "dQw4w9WgXcQ"
}

Response:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "youtube_video_id": "dQw4w9WgXcQ",
  "connected_at": "2024-02-21T10:30:00Z"
}
```

**GET /public-pulse/{movie_id}/sentiment**
```json
Response:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "pulse_score": 75.5,
  "sentiment_breakdown": {
    "positive": 65,
    "negative": 20,
    "neutral": 15
  },
  "video_stats": {
    "views": 1500000,
    "likes": 45000,
    "dislikes": 2000,
    "comments": 3500
  },
  "last_updated": "2024-02-21T10:30:00Z"
}
```


#### Release Strategy Endpoints

**POST /release-strategy/analyze-date-range**
```json
Request:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "target_release_date": "2026-03-15T00:00:00Z",
  "days_before": 30,
  "days_after": 30
}

Response:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "your_movie_title": "Action Hero",
  "your_movie_category": "big",
  "target_release_date": "2026-03-15T00:00:00Z",
  "date_range_start": "2026-02-13T00:00:00Z",
  "date_range_end": "2026-04-14T00:00:00Z",
  "total_competitors": 8,
  "competitors": [
    {
      "movie_id": "507f1f77bcf86cd799439013",
      "title": "Mega Action Hero",
      "director": "S. S. Rajamouli",
      "genre": ["Action", "Drama"],
      "budget": 250000000,
      "release_date": "2026-03-12T00:00:00Z",
      "category": "big",
      "cast_score": 90,
      "historic_score": 85,
      "public_pulse_score": 88,
      "days_from_your_release": 3,
      "threat_level": "high",
      "language": "Telugu",
      "region": "Pan-India"
    }
  ],
  "big_movies_count": 2,
  "medium_movies_count": 4,
  "small_movies_count": 2,
  "high_threat_count": 2,
  "recommendation": "High risk window. 2 high-threat competitors detected...",
  "optimal_release_windows": [
    {
      "start_date": "2026-03-25T00:00:00Z",
      "end_date": "2026-04-05T00:00:00Z",
      "reason": "Clear window with no direct competition"
    }
  ],
  "risk_assessment": "HIGH - Multiple big-budget films in range"
}
```

#### Budget Planning Endpoints

**POST /budget/calculate**
```json
Request:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "total_budget": 50000000,
  "timeline_weeks": 12,
  "allocations": {
    "digital": 35,
    "traditional": 25,
    "influencer": 15,
    "events": 15,
    "pr": 7,
    "contingency": 3
  }
}

Response:
{
  "total_budget": 50000000,
  "timeline_weeks": 12,
  "allocations": {
    "digital": 17500000,
    "traditional": 12500000,
    "influencer": 7500000,
    "events": 7500000,
    "pr": 3500000,
    "contingency": 1500000
  },
  "roi_estimates": {
    "digital": 43750000,
    "traditional": 22500000,
    "influencer": 16500000,
    "events": 11250000,
    "pr": 7000000,
    "contingency": 1500000
  },
  "total_roi": 102500000,
  "roi_multiplier": 2.05
}
```

**POST /budget/optimize**
```json
Request:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "total_budget": 50000000,
  "genre": "Action",
  "target_audience": "Youth",
  "current_allocations": { ... }
}

Response:
{
  "optimized_allocations": {
    "digital": 40,
    "traditional": 20,
    "influencer": 18,
    "events": 12,
    "pr": 7,
    "contingency": 3
  },
  "reasoning": "For Action genre targeting youth audience...",
  "expected_improvement": "15% higher ROI",
  "ai_recommendations": "# Budget Optimization\n\n## Recommended Changes..."
}
```


#### Facebook Campaign Endpoints

**POST /facebook-campaign/generate-poster**
```json
Request:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "prompt": "Action Hero - Epic action drama starring Allu Arjun",
  "style": "cinematic"
}

Response:
{
  "poster_url": "https://gen.pollinations.ai/image?prompt=...",
  "generated_at": "2024-02-21T10:30:00Z"
}
```

**POST /facebook-campaign/post-to-facebook**
```json
Request:
{
  "movie_id": "507f1f77bcf86cd799439012",
  "poster_url": "https://...",
  "caption": "Presenting Action Hero - Coming March 2026!",
  "schedule_time": null
}

Response:
{
  "post_id": "123456789_987654321",
  "posted_at": "2024-02-21T10:30:00Z",
  "status": "published"
}
```

#### Data Analytics Endpoints

**GET /data-analytics/grade-performance**
```json
Response:
{
  "labels": ["Grade 1", "Grade 2", "Grade 3"],
  "data": [7.8, 6.5, 5.2],
  "outliers": [
    {
      "movie": "Baahubali",
      "grade": "Grade 1",
      "rating": 9.2,
      "reason": "Exceeded grade expectation by 1.4 points"
    }
  ]
}
```

**GET /data-analytics/genre-timeline**
```json
Response:
{
  "labels": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023"],
  "datasets": [
    {
      "label": "Action",
      "data": [450, 520, 480, 550]
    },
    {
      "label": "Drama",
      "data": [380, 420, 390, 460]
    }
  ]
}
```

**GET /data-analytics/talent-matrix**
```json
Response:
{
  "datasets": [
    {
      "label": "Allu Arjun",
      "data": [
        {
          "x": 7.5,
          "y": 85,
          "r": 12
        }
      ],
      "backgroundColor": "rgba(59, 130, 246, 0.6)"
    }
  ]
}
```

**GET /data-analytics/demographic-heatmap**
```json
Response:
{
  "genres": ["Action", "Drama", "Comedy", "Romance"],
  "age_groups": ["18-25", "26-35", "36-45", "46+"],
  "data": [
    [0.85, 0.72, 0.45, 0.23],
    [0.65, 0.78, 0.82, 0.55],
    [0.92, 0.88, 0.65, 0.42],
    [0.45, 0.58, 0.72, 0.68]
  ]
}
```

---

## Database Schema

### MongoDB Collections

#### 1. users
```javascript
{
  _id: ObjectId,
  email: String (unique, required),
  username: String (unique, required),
  full_name: String,
  hashed_password: String (required),
  is_active: Boolean (default: true),
  created_at: DateTime (default: now)
}

Indexes:
- email (unique)
- username (unique)
```


#### 2. movies
```javascript
{
  _id: ObjectId,
  title: String (required),
  director: String (required),
  genres: [String] (required),
  budget: Number,
  budget_currency: String (default: "INR"),
  release_date: DateTime,
  languages: [String] (required),
  region: String (required),
  cast: [
    {
      name: String,
      role: String,
      star_power: Number
    }
  ],
  producer_id: String (required, ref: users._id),
  status: String (enum: pre-production, production, post-production, awaiting-release, released),
  tag: String (enum: current, past),
  created_at: DateTime (default: now),
  updated_at: DateTime (default: now),
  
  // Scores
  hws_score: Number,
  cast_score: Number,
  historic_score: Number,
  public_pulse_score: Number,
  
  // YouTube integration
  youtube_video_id: String,
  sentiment_history: [
    {
      timestamp: DateTime,
      pulse_score: Number,
      sentiment_breakdown: {
        positive: Number,
        negative: Number,
        neutral: Number
      },
      video_stats: {
        views: Number,
        likes: Number,
        dislikes: Number,
        comments: Number
      }
    }
  ]
}

Indexes:
- producer_id
- release_date
- tag
- status
- { producer_id: 1, tag: 1 }
- { release_date: 1, status: 1 }
```

#### 3. pr_strategies
```javascript
{
  _id: ObjectId,
  movie_id: String (required, ref: movies._id),
  producer_id: String (required, ref: users._id),
  strategy: {
    strategy: String,
    key_differentiators: [String],
    target_audience_approach: Object,
    media_channels: [Object],
    timeline: [Object],
    budget_allocation: Object,
    risk_mitigation: [String],
    success_metrics: [String]
  },
  created_at: DateTime (default: now)
}

Indexes:
- movie_id
- producer_id
- created_at
```

#### 4. facebook_campaigns
```javascript
{
  _id: ObjectId,
  movie_id: String (required, ref: movies._id),
  producer_id: String (required, ref: users._id),
  poster_url: String,
  caption: String,
  facebook_post_id: String,
  status: String (enum: draft, scheduled, published, failed),
  scheduled_time: DateTime,
  posted_at: DateTime,
  created_at: DateTime (default: now)
}

Indexes:
- movie_id
- producer_id
- status
- scheduled_time
```

#### 5. budget_plans
```javascript
{
  _id: ObjectId,
  movie_id: String (required, ref: movies._id),
  producer_id: String (required, ref: users._id),
  total_budget: Number (required),
  timeline_weeks: Number (required),
  allocations: {
    digital: Number,
    traditional: Number,
    influencer: Number,
    events: Number,
    pr: Number,
    contingency: Number
  },
  roi_estimates: Object,
  ai_recommendations: String,
  created_at: DateTime (default: now),
  updated_at: DateTime (default: now)
}

Indexes:
- movie_id
- producer_id
```


### ChromaDB Collections

#### historical_movies
```javascript
{
  id: String (UUID),
  metadata: {
    movie_name: String,
    hero: String,
    heroine: String,
    director: String,
    budget: Number,
    revenue: Number,
    imdb_rating: Number,
    popularity_score: Number,
    genre: String,
    release_date: String,
    tag: "past"
  },
  embedding: [Number] (vector),
  document: String (text representation)
}

Purpose: Semantic search for similar historical movies
```

---

## Deployment Guide

### Prerequisites
- Python 3.11+
- Node.js 18+
- MongoDB 4.6+
- Ollama (for local LLM)

### Backend Deployment

#### 1. Environment Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 2. Environment Variables
Create `.env` file:
```env
# MongoDB
MONGO_URI=mongodb://localhost:27017/film_intel_db

# External APIs
YOUTUBE_API_KEY=your_youtube_api_key
OLLAMA_BASE_URL=http://localhost:11434
DEEPSEEK_API_KEY=your_deepseek_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret

# JWT
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Facebook
FACEBOOK_PAGE_ACCESS_TOKEN=your_facebook_page_token
FACEBOOK_PAGE_ID=your_facebook_page_id
```

#### 3. Database Setup
```bash
# Start MongoDB
mongod --dbpath /path/to/data

# Seed historical data
python scripts/ingest_csv.py
python scripts/seed_vector_db.py

# Create test data
python scripts/seed_current_movies_existing.py
```

#### 4. Start Backend Server
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend Deployment

#### 1. Environment Setup
```bash
cd frontend_new
npm install
```

#### 2. Environment Variables
Create `.env` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

#### 3. Development Server
```bash
npm run dev
```

#### 4. Production Build
```bash
npm run build
npm run preview
```

### Production Deployment

#### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

#### Docker Compose
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:4.6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGO_URI=mongodb://mongodb:27017/film_intel_db
    depends_on:
      - mongodb
  
  frontend:
    build: ./frontend_new
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mongo_data:
```


### Ollama Setup (Local LLM)

#### 1. Install Ollama
```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

#### 2. Pull DeepSeek R1 Model
```bash
ollama pull deepseek-r1:7b
```

#### 3. Verify Installation
```bash
ollama list
ollama run deepseek-r1:7b "Hello"
```

### Nginx Configuration (Production)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Frontend
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }
    
    # Backend API
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL Configuration (Let's Encrypt)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Testing

### Backend Testing
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest tests/

# With coverage
pytest --cov=app tests/
```

### Frontend Testing
```bash
# Install test dependencies
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest

# Run tests
npm run test

# With coverage
npm run test:coverage
```

### API Testing
Use Postman collection or curl:
```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test@123"}'

# Get movies
curl -X GET http://localhost:8000/api/v1/movies \
  -H "Authorization: Bearer <token>"
```

---

## Monitoring & Logging

### Backend Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Error Tracking
- Sentry integration for error monitoring
- Custom error handlers in FastAPI
- Structured logging with JSON format

### Performance Monitoring
- Response time tracking
- Database query profiling
- API endpoint metrics
- Resource usage monitoring

---

## Security Best Practices

### 1. Authentication
- Strong password requirements (min 8 chars, uppercase, lowercase, number, special char)
- JWT token expiry (24 hours)
- Refresh token mechanism
- Rate limiting on auth endpoints

### 2. Data Protection
- Password hashing with bcrypt (cost factor 12)
- Environment variables for secrets
- HTTPS in production
- CORS configuration
- Input sanitization

### 3. API Security
- Request validation with Pydantic
- SQL injection prevention (NoSQL)
- XSS protection
- CSRF tokens for state-changing operations
- API rate limiting

### 4. Database Security
- MongoDB authentication
- Connection string encryption
- Regular backups
- Access control lists
- Audit logging


---

## Performance Optimization

### Backend Optimization
1. **Async Operations**: All I/O operations use async/await
2. **Database Indexing**: Indexes on frequently queried fields
3. **Connection Pooling**: MongoDB connection pool
4. **Caching**: Redis for frequently accessed data
5. **Query Optimization**: Projection to fetch only required fields
6. **Pagination**: Limit results for large datasets

### Frontend Optimization
1. **Code Splitting**: Route-based lazy loading
2. **Bundle Optimization**: Vite tree-shaking
3. **Image Optimization**: Lazy loading, WebP format
4. **Memoization**: React.memo for expensive components
5. **Virtual Scrolling**: For large lists
6. **Debouncing**: Search inputs, API calls

---

## Troubleshooting

### Common Issues

#### 1. MongoDB Connection Failed
```bash
# Check MongoDB status
sudo systemctl status mongod

# Restart MongoDB
sudo systemctl restart mongod

# Check connection string
echo $MONGO_URI
```

#### 2. Ollama Not Responding
```bash
# Check Ollama status
ollama list

# Restart Ollama
ollama serve

# Check model
ollama run deepseek-r1:7b "test"
```

#### 3. CORS Errors
- Verify frontend URL in backend CORS configuration
- Check browser console for specific error
- Ensure credentials are included in requests

#### 4. JWT Token Expired
- Token expires after 24 hours
- Implement refresh token mechanism
- Clear localStorage and re-login

#### 5. Facebook API Errors
- Verify Page Access Token validity
- Check token permissions
- Ensure Page ID is correct

---

## Future Enhancements

### Planned Features
1. **Real-time Notifications**: WebSocket for live updates
2. **Mobile App**: React Native version
3. **Advanced Analytics**: Predictive modeling with ML
4. **Multi-language Support**: i18n implementation
5. **Collaboration**: Multi-user producer teams
6. **Export Reports**: PDF/Excel generation
7. **Integration**: Box office data APIs
8. **Social Media**: Twitter, Instagram integration
9. **Voice Assistant**: Voice commands for queries
10. **Blockchain**: NFT integration for movie rights

### Technical Improvements
1. **Microservices**: Break into smaller services
2. **GraphQL**: Alternative to REST API
3. **Server-Side Rendering**: Next.js migration
4. **Progressive Web App**: Offline support
5. **CI/CD Pipeline**: Automated testing and deployment
6. **Load Balancing**: Multiple backend instances
7. **CDN**: Static asset delivery
8. **Kubernetes**: Container orchestration

---

## Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Standards
- **Backend**: PEP 8 style guide
- **Frontend**: ESLint + Prettier
- **Commits**: Conventional Commits format
- **Documentation**: Docstrings for all functions
- **Testing**: Unit tests for new features

---

## License

This project is proprietary software. All rights reserved.

---

## Support

### Documentation
- API Documentation: `/docs` (Swagger UI)
- Technical Support: support@filmintel.com
- Bug Reports: GitHub Issues

### Contact
- Email: info@filmintel.com
- Website: https://filmintel.com
- Twitter: @FilmIntelPlatform

---

## Acknowledgments

- **FastAPI**: Modern Python web framework
- **React**: UI library
- **MongoDB**: Database solution
- **Ollama**: Local LLM infrastructure
- **DeepSeek**: AI model for recommendations
- **Pollinations AI**: Image generation
- **YouTube API**: Sentiment data source
- **Chart.js**: Data visualization
- **TailwindCSS**: Styling framework

---

## Version History

### v1.0.0 (Current)
- Initial release
- Core features: HWS, Public Pulse, Release Strategy
- Budget Planning with AI optimization
- Facebook Campaign automation
- Data Analytics dashboard
- Competitor analysis

### Roadmap
- v1.1.0: Real-time notifications, Mobile app
- v1.2.0: Advanced ML models, Multi-language
- v2.0.0: Microservices architecture, GraphQL

---

**Last Updated**: February 21, 2026
**Maintained By**: Film Intel Development Team
