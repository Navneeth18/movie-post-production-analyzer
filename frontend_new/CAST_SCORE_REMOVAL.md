# Cast Score Removal & Historical Movie Restrictions

## Changes Made

### 1. Removed Cast Score Display

Cast score has been removed from all frontend displays. Only HWS (Historical Weighted Score) is now shown.

#### Files Updated:
- `src/pages/Movies.jsx` - Movie cards now show only HWS score
- `src/pages/Dashboard.jsx` - Dashboard stats show "Avg HWS Score" instead of "Avg Cast Score"
- `src/pages/MovieDetail.jsx` - Movie detail page shows only HWS score (removed cast score card)

#### What Changed:
**Before:**
- Movie cards showed: Cast Score | HWS Score
- Dashboard showed: Avg Cast Score
- Movie detail showed: Cast Score card + HWS Score card

**After:**
- Movie cards show: HWS Score only (with category badge)
- Dashboard shows: Avg HWS Score
- Movie detail shows: HWS Score only (full width, with category badge)

### 2. Hidden Features for Historical Movies

Historical movies (tag="past") no longer show buttons for:
- Public Pulse Analytics
- Analyze Competitors
- Release Strategy

#### Files Updated:
- `src/pages/MovieDetail.jsx` - Conditionally renders action buttons based on movie tag

#### Implementation:
```javascript
{movie.tag === 'current' && (
  <>
    <Link to={`/movies/${id}/public-pulse`}>Public Pulse Analytics</Link>
    <Link to={`/movies/${id}/competitors`}>Analyze Competitors</Link>
    <Link to={`/movies/${id}/release-analysis`}>Release Strategy</Link>
  </>
)}

{movie.tag === 'past' && (
  <div className="text-center py-4 bg-gray-50 rounded-lg">
    <p>This is a historical movie. These features are only available for current movies.</p>
  </div>
)}
```

### 3. Backend Already Restricts Historical Movies

The backend already has restrictions in place (implemented earlier):
- Public Pulse endpoints return 400 error for historical movies
- Competitor analysis endpoints return 400 error for historical movies
- Release strategy endpoints return 400 error for historical movies

## Movie Tag System

### Current Movies (tag="current")
- ✅ Can view HWS score and breakdown
- ✅ Can add YouTube trailer for Public Pulse
- ✅ Can analyze competitors
- ✅ Can use release strategy tools
- ✅ Can edit movie details

### Historical Movies (tag="past")
- ✅ Can view HWS score and breakdown
- ✅ Can view all movie details
- ❌ Cannot use Public Pulse (no trailer needed)
- ❌ Cannot analyze competitors (already released)
- ❌ Cannot use release strategy (already released)
- ❌ Cannot edit (read-only)

## Visual Changes

### Movie Cards
```
Before:
┌─────────────────┐
│ Movie Title     │
│ Cast: 64        │
│ HWS: 76         │
└─────────────────┘

After:
┌─────────────────┐
│ Movie Title     │
│ HWS: 76 [BIG]   │
└─────────────────┘
```

### Movie Detail Page
```
Before:
┌──────────────┐ ┌──────────────┐
│ Cast Score   │ │ HWS Score    │
│    64.0      │ │   76.7 [BIG] │
└──────────────┘ └──────────────┘

After:
┌────────────────────────────────┐
│ HWS Score                      │
│   76.7 [BIG]                   │
│ Global theatrical release...   │
└────────────────────────────────┘
```

### Historical Movie Detail
```
Before:
[Public Pulse] [Competitors] [Strategy]

After (Historical):
┌────────────────────────────────────────┐
│ This is a historical movie.            │
│ These features are only available      │
│ for current movies.                    │
└────────────────────────────────────────┘
```

## HWS Score Calculation

HWS is still calculated using cast data internally, but the cast score is no longer displayed separately. The HWS formula includes:

- Director (25%)
- Genre (20%)
- Hero (15%)
- Popularity (15%)
- Predicted IMDb (10%)
- Heroine (8%)
- Producer (7%)

The cast (hero/heroine) scores are part of the HWS calculation but are not shown as a separate metric.

## Testing

To verify the changes:

1. **View Current Movie**: Should see HWS score and all action buttons
2. **View Historical Movie**: Should see HWS score but NO action buttons
3. **Dashboard**: Should show "Avg HWS Score" instead of "Avg Cast Score"
4. **Movie Cards**: Should show only HWS score with category badge

## Benefits

1. **Simplified UI**: Users see one main score (HWS) instead of multiple scores
2. **Clear Restrictions**: Historical movies clearly show they don't have access to planning features
3. **Better UX**: Users won't try to use features that don't make sense for released movies
4. **Consistent**: Frontend restrictions match backend restrictions
