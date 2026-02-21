# Quick Start: Budget Planning with DeepSeek R1

## Prerequisites

1. **Ollama Running** with DeepSeek R1:
   ```bash
   ollama serve
   ollama pull deepseek-r1:7b
   ```

2. **Backend Running**:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

3. **Frontend Running**:
   ```bash
   cd frontend_new
   npm run dev
   ```

## Using Budget Planning

### Step 1: Access Budget Planning
1. Login as a producer
2. Go to any current movie (not historical)
3. Click **"Budget Planning"** button

### Step 2: Set Total Budget
- Use slider to set marketing budget (₹10L - ₹50Cr)
- Default: ₹50L (₹5,000,000)

### Step 3: Allocate Budget
Adjust sliders for 6 channels:
- **Digital Marketing** (25-35% optimal)
- **Traditional Media** (10-20% optimal)
- **Influencer Marketing** (15-25% optimal)
- **Events & Activations** (8-15% optimal)
- **PR & Media Relations** (10-20% optimal)
- **Contingency Reserve** (10-15% optimal)

### Step 4: Set Timeline
- Use slider to set campaign duration (4-16 weeks)
- Default: 8 weeks before release

### Step 5: View Projections
Real-time metrics update automatically:
- **Allocated**: Total percentage (aim for 95-100%)
- **Projected ROI**: Expected return multiplier
- **Health Status**: Optimal/Under-allocated/Over Budget

### Step 6: Apply Optimal (Optional)
Click **"Apply Optimal"** for genre-specific preset:
- Action/Thriller: High digital focus
- Drama/Romance: High PR & influencer
- Comedy/Family: Balanced with events

### Step 7: AI Optimization (Optional)
1. Click **"Generate AI Optimization Strategy"**
2. Wait 2-3 minutes (DeepSeek R1 reasoning)
3. Review comprehensive recommendations:
   - Budget reallocation suggestions
   - Channel-specific tactics
   - Timeline strategy
   - Risk mitigation
   - ROI improvements

### Step 8: Save
Click **"Save Budget Plan"** to persist to database

## Quick Tips

### Optimal Allocation
- Keep total at 95-100% for efficiency
- Respect minimum budgets per channel
- Higher ROI channels = better returns

### Channel Selection
- **Digital** (3.2x ROI): Best for viral potential
- **PR** (2.8x ROI): Critical for word-of-mouth
- **Influencer** (2.5x ROI): Growing importance
- **Events** (2.0x ROI): Direct engagement
- **Traditional** (1.8x ROI): Mass reach
- **Contingency** (0x ROI): Safety net

### Timeline Strategy
- **Longer campaigns** (12-16 weeks): Spread awareness
- **Shorter campaigns** (4-6 weeks): Concentrated impact
- **Standard** (8 weeks): Balanced approach

### AI Optimization
- Takes 2-3 minutes (chain-of-thought reasoning)
- Provides genre-specific insights
- Falls back to rules if timeout
- Best used after initial allocation

## Troubleshooting

### "AI Optimization Failed"
**Cause**: Ollama not running or DeepSeek R1 not installed
**Fix**:
```bash
ollama serve
ollama pull deepseek-r1:7b
```

### "Total allocation over 100%"
**Cause**: Channel percentages sum > 100%
**Fix**: Reduce one or more channel allocations

### "Below minimum recommended budget"
**Cause**: Channel allocation too low for effectiveness
**Fix**: Increase allocation or set to 0% to disable

### "Budget planning only for current movies"
**Cause**: Trying to access for historical movie
**Fix**: Only use with movies tagged as "current"

## Example Allocations

### Action Movie (₹5Cr budget)
```
Digital:      38% (₹1.90Cr) - YouTube, Social ads
Traditional:  10% (₹0.50Cr) - TV spots
Influencer:   22% (₹1.10Cr) - Gaming influencers
Events:       10% (₹0.50Cr) - Fan meetups
PR:           12% (₹0.60Cr) - Media coverage
Contingency:   8% (₹0.40Cr) - Emergency fund

Projected ROI: 2.6x
Expected Return: ₹13Cr
```

### Drama Movie (₹3Cr budget)
```
Digital:      28% (₹0.84Cr) - Instagram, Facebook
Traditional:  12% (₹0.36Cr) - Print ads
Influencer:   22% (₹0.66Cr) - Lifestyle influencers
Events:       12% (₹0.36Cr) - Premiere events
PR:           18% (₹0.54Cr) - Reviews, interviews
Contingency:   8% (₹0.24Cr) - Emergency fund

Projected ROI: 2.5x
Expected Return: ₹7.5Cr
```

### Comedy Movie (₹4Cr budget)
```
Digital:      35% (₹1.40Cr) - Viral content
Traditional:  12% (₹0.48Cr) - Radio, outdoor
Influencer:   25% (₹1.00Cr) - Comedy creators
Events:       15% (₹0.60Cr) - Mall activations
PR:            8% (₹0.32Cr) - Media coverage
Contingency:   5% (₹0.20Cr) - Emergency fund

Projected ROI: 2.7x
Expected Return: ₹10.8Cr
```

## API Testing

### Test Budget Schemas
```bash
cd backend
python test_budget_api.py
```

### Test DeepSeek R1
```bash
cd backend
python test_deepseek_budget.py
```

### Test via API
```bash
# Get budget plan
curl http://localhost:8000/api/v1/budget/{movie_id}/budget-plan \
  -H "Authorization: Bearer {token}"

# Create budget plan
curl -X POST http://localhost:8000/api/v1/budget/{movie_id}/budget-plan \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'

# AI optimization
curl -X POST http://localhost:8000/api/v1/budget/{movie_id}/budget-plan/optimize \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "movie_title": "Leo 2",
    "genre": "Action",
    "budget": 50000000,
    "total_marketing_budget": 5000000,
    "timeline_weeks": 8,
    "current_allocations": {...}
  }'
```

## Key Metrics

- **Optimal Allocation**: 95-100%
- **Average ROI**: 2.35x (default allocation)
- **Best ROI Channel**: Digital (3.2x)
- **Minimum Contingency**: 5-10%
- **AI Processing Time**: 120-180 seconds

## Support

For issues or questions:
1. Check `BUDGET_PLANNING_MODULE.md` for detailed docs
2. Review `FINAL_IMPLEMENTATION_SUMMARY.md` for technical details
3. Test with provided scripts in `backend/test_*.py`
