# HWS (Historical Weighted Score) Implementation

## Overview
The HWS system uses exponential grading and market-adjusted weights to predict movie success and categorize films into BIG, MEDIUM, or SMALL categories.

## Formula

```
HWS = (W_d × S_d) + (W_h × S_h) + (W_g × S_g) + (W_v × S_v) + 
      (W_i × S_i) + (W_f × S_f) + (W_p × S_p)
```

### Weights (Market Impact)
- **Director (W_d)**: 25% - Director's brand is primary trust factor
- **Genre (W_g)**: 20% - Trending genre has higher audience floor
- **Hero (W_h)**: 15% - Initial 3-day theatrical opening pull
- **Popularity (W_v)**: 15% - Real-time interest (Pulse metric)
- **Predicted IMDb (W_i)**: 10% - Long-term OTT value
- **Heroine (W_f)**: 8% - Chemistry and visual appeal
- **Producer (W_p)**: 7% - Resources for distribution and scale

### Exponential Grading Scale
- **Grade 1 (Elite)**: Score = 100
- **Grade 2 (Established)**: Score = 40
- **Grade 3 (Newcomer/Budding)**: Score = 10

This exponential scale ensures that Grade 1 artists contribute significantly more than Grade 3 artists, creating clear differentiation between BIG and SMALL movies.

## Categorization

| HWS Range | Category | Market Action |
|-----------|----------|---------------|
| 75-100 | BIG | Global theatrical release; Massive marketing spend |
| 45-74 | MEDIUM | Targeted regional release; High PR influencer focus |
| 0-44 | SMALL | OTT-First strategy or hyper-niche community marketing |

## Implementation

### Backend Components

1. **HWSCalculator** (`app/services/hws_calculator.py`)
   - Core calculation engine
   - Fetches artist grades from database
   - Calculates individual component scores
   - Returns HWS score, category, and detailed breakdown

2. **Artist Database** (`artists` collection)
   - Contains 1,554 artists from BOB dataset
   - Roles: Director, Lead 1 (Hero), Lead 2 (Heroine), Producer
   - Grades: Grade 1 (23), Grade 2 (17), Grade 3 (1,514)

3. **Movie Endpoints** (`app/api/endpoints/movies.py`)
   - Automatically calculates HWS on movie creation
   - Recalculates for historical movies on fetch
   - Returns HWS breakdown for detailed analysis

### Database Schema

#### Current Movies (`movies` collection)
```json
{
  "title": "Movie Name",
  "director": "Director Name",
  "genres": ["Action", "Drama"],
  "cast": [
    {"name": "Actor Name", "role": "Hero"},
    {"name": "Actress Name", "role": "Heroine"}
  ],
  "cast_score": 64.0,
  "hws_score": 76.7,
  "category": "BIG",
  "market_action": "Global theatrical release...",
  "hws_breakdown": {
    "director_score": 100,
    "director_contribution": 25.0,
    "hero_score": 100,
    "hero_contribution": 15.0,
    ...
  }
}
```

#### Historical Movies (`historical_movies` collection)
- Linked to producer accounts via migration
- HWS calculated on-the-fly using hero/heroine from database
- Uses budget/revenue to estimate popularity score

### Frontend Components

1. **Movie Cards** (`Movies.jsx`, `Dashboard.jsx`)
   - Display Cast Score and HWS Score
   - Show category badge (BIG/MEDIUM/SMALL)
   - Color-coded by category

2. **Movie Detail Page** (`MovieDetail.jsx`)
   - Full HWS breakdown visualization
   - 7 component cards showing individual contributions
   - Category badge with market action description

## Testing

### Test Scripts

1. **check_artists.py** - Verify artists collection
2. **test_hws_calculation.py** - Test HWS calculator directly
3. **test_complete_hws_flow.py** - Test end-to-end flow
4. **test_api_hws.py** - Test through API endpoints

### Running Tests

```bash
# Check artists database
python check_artists.py

# Test HWS calculation
python test_hws_calculation.py

# Test complete flow
python test_complete_hws_flow.py

# Test API (requires backend running)
python test_api_hws.py
```

## Example Results

### BIG Movie (Rajamouli + Prabhas)
- Director Score: 100 (Grade 1) → Contribution: 25.0
- Hero Score: 100 (Grade 1) → Contribution: 15.0
- Genre Score: 90 (Action) → Contribution: 18.0
- **Total HWS: 81.95** → **Category: BIG**

### MEDIUM Movie (Parasuram + Vijay Deverakonda)
- Director Score: 10 (Grade 3) → Contribution: 2.5
- Hero Score: 40 (Grade 2) → Contribution: 6.0
- Genre Score: 70 (Drama) → Contribution: 14.0
- **Total HWS: 36.0** → **Category: SMALL**

### SMALL Movie (Unknown Director + New Actors)
- Director Score: 10 (Grade 3) → Contribution: 2.5
- Hero Score: 10 (Grade 3) → Contribution: 1.5
- Genre Score: 65 (Romance) → Contribution: 13.0
- **Total HWS: 27.15** → **Category: SMALL**

## Key Features

✅ Exponential grading creates clear differentiation
✅ Market-adjusted weights reflect current industry trends
✅ Automatic calculation on movie creation
✅ Historical movies calculate HWS from database artists
✅ Detailed breakdown for transparency
✅ Category-based marketing recommendations
✅ Frontend visualization with color-coded badges

## Future Enhancements

- [ ] Update popularity score from Public Pulse analytics
- [ ] Add genre trending scores based on market data
- [ ] Implement director historical average for predicted IMDb
- [ ] Add producer grade impact on distribution scale
- [ ] Create HWS comparison tool for competitor analysis
