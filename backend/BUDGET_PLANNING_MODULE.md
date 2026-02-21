# Budget Planning Module

## Overview
The Budget Planning module helps producers strategically allocate their marketing budget across different channels and optimize ROI for movie promotions using AI-powered recommendations from DeepSeek R1.

## Features

### 1. Budget Allocation
- **Total Budget**: Set marketing budget (₹10L - ₹50Cr)
- **Channel Allocation**: Distribute budget across 6 channels:
  - Digital Marketing (25-35% optimal)
  - Traditional Media (10-20% optimal)
  - Influencer Marketing (15-25% optimal)
  - Events & Activations (8-15% optimal)
  - PR & Media Relations (10-20% optimal)
  - Contingency Reserve (10-15% optimal)

### 2. Timeline Planning
- Configure campaign duration (4-16 weeks before release)
- Automatic spending breakdown:
  - Weeks 8-6: Awareness Phase (25%)
  - Weeks 5-3: Interest Phase (35%)
  - Weeks 2-1: Desire Phase (30%)
  - Week 0: Action Phase (10%)

### 3. ROI Projection
- Real-time ROI calculation based on channel performance
- Channel-specific ROI multipliers:
  - Digital: 3.2x
  - PR: 2.8x
  - Influencer: 2.5x
  - Events: 2.0x
  - Traditional: 1.8x
  - Contingency: 0x

### 4. AI Optimization (DeepSeek R1)
- **Powered by DeepSeek R1:7b** via Ollama
- Genre-specific recommendations
- Channel-specific tactics
- Timeline-based spending strategy
- Risk mitigation suggestions
- Expected ROI improvements
- **Processing Time**: 2-3 minutes (due to chain-of-thought reasoning)
- **Fallback**: Rule-based recommendations if AI unavailable or times out

### 5. Optimal Allocation Presets
- **Drama/Romance**: Higher PR & Influencer focus
- **Action/Thriller/Sci-Fi**: Maximum digital spend
- **Comedy/Family**: Balanced with events emphasis

## API Endpoints

### Create/Update Budget Plan
```
POST /api/v1/budget/{movie_id}/budget-plan
```

**Request Body:**
```json
{
  "total_budget": 5000000,
  "allocations": {
    "digital": 30,
    "traditional": 15,
    "influencer": 20,
    "events": 10,
    "pr": 15,
    "contingency": 10
  },
  "timeline_weeks": 8
}
```

**Response:**
```json
{
  "id": "budget_plan_id",
  "movie_id": "movie_id",
  "producer_id": "producer_id",
  "total_budget": 5000000,
  "allocations": {...},
  "timeline_weeks": 8,
  "total_allocated_percentage": 100,
  "projected_roi": 2.35,
  "projected_revenue": 11750000,
  "created_at": "2026-02-21T...",
  "updated_at": "2026-02-21T..."
}
```

### Get Budget Plan
```
GET /api/v1/budget/{movie_id}/budget-plan
```

### AI Optimization
```
POST /api/v1/budget/{movie_id}/budget-plan/optimize
```

**Request Body:**
```json
{
  "movie_title": "Leo 2",
  "genre": "Action",
  "budget": 50000000,
  "total_marketing_budget": 5000000,
  "timeline_weeks": 8,
  "current_allocations": {...}
}
```

## Frontend Routes

- `/movies/:id/budget-planning` - Budget planning interface

## Database Schema

### Collection: `budget_plans`
```javascript
{
  _id: ObjectId,
  movie_id: String,
  producer_id: String,
  total_budget: Number,
  allocations: {
    digital: Number,
    traditional: Number,
    influencer: Number,
    events: Number,
    pr: Number,
    contingency: Number
  },
  timeline_weeks: Number,
  total_allocated_percentage: Number,
  projected_roi: Number,
  projected_revenue: Number,
  created_at: Date,
  updated_at: Date
}
```

## Usage Flow

1. Producer navigates to movie detail page
2. Clicks "Budget Planning" button
3. Sets total marketing budget
4. Adjusts channel allocations using sliders
5. Configures timeline (weeks before release)
6. Views real-time ROI projections
7. Optionally applies genre-specific optimal allocation
8. Optionally generates AI optimization recommendations
9. Saves budget plan

## Validation Rules

- Total budget must be > 0
- Each channel allocation: 0-50%
- Timeline: 4-16 weeks
- Warning if total allocation > 100%
- Warning if channel allocation < minimum recommended budget

## Features Restricted to Current Movies

Budget planning is only available for movies with `tag: "current"`. Historical movies cannot access this feature.

## AI Optimization

The AI optimization provides:
1. Budget reallocation recommendations
2. Genre-specific channel tactics
3. Timeline-based spending breakdown
4. Risk mitigation strategies
5. Expected ROI improvements

Falls back to rule-based recommendations if AI service is unavailable.

## Channel Details

Each channel provides:
- Sub-channel breakdown
- Average ROI multiplier
- Minimum recommended budget
- Optimal allocation range
- Projected return calculation

## Best Practices

1. **Start with Optimal**: Use genre-specific presets as baseline
2. **Monitor Allocation**: Keep total at 95-100% for maximum efficiency
3. **Respect Minimums**: Ensure each active channel meets minimum budget
4. **Save Regularly**: Budget plans auto-save on update
5. **Use AI Insights**: Generate optimization for data-driven decisions
6. **Adjust Timeline**: Longer campaigns need different allocation strategies

## Integration Points

- **Movie Model**: Links to movie via `movie_id`
- **User Auth**: Validates producer ownership
- **AI Service**: Optional optimization recommendations
- **Dashboard**: Can display budget metrics (future enhancement)

## Future Enhancements

- Historical performance tracking
- A/B testing recommendations
- Real-time spend tracking
- Integration with actual campaign performance
- Competitor budget benchmarking
- Regional allocation strategies
