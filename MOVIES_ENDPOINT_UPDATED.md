# ✅ Movies Endpoint Updated - Now Includes Historical Movies!

## What Changed

The main `/api/v1/movies/` endpoint now returns **both current and historical movies** for the logged-in producer.

## API Endpoint Details

### GET `/api/v1/movies/`

**Query Parameters:**
- `include_historical` (optional, default: `true`) - Set to `false` to get only current movies

**Returns:**
Combined list of movies from both collections:
- Current projects from `movies` collection
- Historical movies from `historical_movies` collection

**Response Format:**
```json
[
  {
    "id": "...",
    "title": "Movie Title",
    "director": "Director Name",
    "genre": "Action, Drama",
    "budget": 47000000,
    "revenue": 21915000,
    "release_date": "09-01-2025",
    "status": "released",
    "tag": "past",
    "imdb_rating": 7.5,
    "hero": "Actor Name",
    "heroine": "Actress Name",
    "source": "historical"  // or "current"
  }
]
```

## Field Mapping

### Historical Movies (from `historical_movies` collection)
- `title` ← `movie_name`
- `status` = `"released"`
- `tag` = `"past"`
- `source` = `"historical"`
- Includes: `hero`, `heroine`, `imdb_rating`, `popularity_score`, `revenue`

### Current Movies (from `movies` collection)
- `title` ← `title`
- `status` ← `status` (pre-production, production, etc.)
- `tag` ← `tag` (current or past)
- `source` = `"current"`
- Includes: `cast_score`, `historic_score`, `public_pulse_score`

## Usage Examples

### Get All Movies (Current + Historical)
```javascript
// Frontend
const response = await movieAPI.getMyMovies();
const allMovies = response.data;

// Separate by source
const currentProjects = allMovies.filter(m => m.source === 'current');
const historicalMovies = allMovies.filter(m => m.source === 'historical');
```

### Get Only Current Movies
```javascript
const response = await api.get('/movies/?include_historical=false');
const currentMovies = response.data;
```

### Get Only Historical Movies
```javascript
const response = await api.get('/movies/historical');
const historicalMovies = response.data;
```

## Test Results

### Dil Raju Account
- **Total Movies**: 5
- **Current Projects**: 0
- **Historical Movies**: 5
  1. The Family Star (2024)
  2. Game Changer (2025)
  3. Shaakuntalam (2023)
  4. Sankranthiki Vasthunam (2025)
  5. Thammudu (2025)

### Prasad Devineni Account
- **Total Movies**: 1
- **Historical Movies**: 1
  1. Bāhubali: The Epic (2025)

## Frontend Integration

Update your Movies page to display both types:

```jsx
import { useState, useEffect } from 'react';
import { movieAPI } from '../services/api';

function MyMovies() {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await movieAPI.getMyMovies();
        setMovies(response.data);
      } catch (error) {
        console.error('Failed to fetch movies:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchMovies();
  }, []);

  // Separate movies by source
  const currentProjects = movies.filter(m => m.source === 'current');
  const historicalMovies = movies.filter(m => m.source === 'historical');

  return (
    <div>
      <h2>Current Projects ({currentProjects.length})</h2>
      {currentProjects.map(movie => (
        <MovieCard key={movie.id} movie={movie} />
      ))}

      <h2>Historical Movies ({historicalMovies.length})</h2>
      {historicalMovies.map(movie => (
        <HistoricalMovieCard key={movie.id} movie={movie} />
      ))}
    </div>
  );
}
```

## Dashboard Statistics

You can now show comprehensive stats:

```javascript
const stats = {
  totalMovies: movies.length,
  currentProjects: movies.filter(m => m.source === 'current').length,
  historicalMovies: movies.filter(m => m.source === 'historical').length,
  totalRevenue: movies
    .filter(m => m.revenue)
    .reduce((sum, m) => sum + m.revenue, 0),
  avgIMDB: movies
    .filter(m => m.imdb_rating)
    .reduce((sum, m) => sum + m.imdb_rating, 0) / 
    movies.filter(m => m.imdb_rating).length
};
```

## Available Endpoints

1. **GET `/api/v1/movies/`** - All movies (current + historical)
2. **GET `/api/v1/movies/?include_historical=false`** - Only current movies
3. **GET `/api/v1/movies/historical`** - Only historical movies (detailed format)
4. **GET `/api/v1/movies/all?tag=current`** - All current movies in system (for competitor analysis)
5. **GET `/api/v1/movies/all?tag=past`** - All past movies in system

## Testing

Run the test script:
```bash
cd backend
python test_combined_movies.py dilraju@gmail.com
```

## Next Steps

1. ✅ Update frontend to display historical movies
2. ✅ Add filtering/sorting by source, date, revenue
3. ✅ Show statistics dashboard with historical data
4. ✅ Add charts for revenue trends over time
5. ✅ Compare current project with historical performance

---

**The `/movies` endpoint now provides complete access to both current and historical movies!** 🎬
