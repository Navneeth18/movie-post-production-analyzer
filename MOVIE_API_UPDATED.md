# ✅ Movie API Updated - Multiple Genres/Languages & Edit Support

## Changes Made

### 1. Multiple Genres Support
- **Before**: Single `genre` field (string)
- **After**: Multiple `genres` field (array of strings)

### 2. Multiple Languages Support
- **Before**: Single `language` field (string)
- **After**: Multiple `languages` field (array of strings)

### 3. Removed Themes
- **Before**: Had `themes` field
- **After**: Removed `themes` field completely

### 4. Full Edit Support
- Can now update any field including:
  - Status (pre-production → production → post-production → awaiting-release → released)
  - Release date
  - Genres and languages
  - Budget, director, cast, etc.

## API Endpoints

### Create Movie
```
POST /api/v1/movies/
```

**Request Body:**
```json
{
  "title": "Movie Title",
  "director": "Director Name",
  "genres": ["Action", "Drama", "Thriller"],
  "languages": ["Telugu", "Hindi", "Tamil"],
  "budget": 50000000,
  "budget_currency": "INR",
  "release_date": "2026-12-25T00:00:00",
  "region": "Pan-India",
  "status": "pre-production",
  "cast": [
    {
      "name": "Actor Name",
      "role": "Hero",
      "star_power": 85
    }
  ]
}
```

**Response:**
```json
{
  "id": "6998e6f5b6fc206c656fc936",
  "title": "Movie Title",
  "director": "Director Name",
  "genres": ["Action", "Drama", "Thriller"],
  "languages": ["Telugu", "Hindi", "Tamil"],
  "budget": 50000000,
  "budget_currency": "INR",
  "release_date": "2026-12-25T00:00:00",
  "region": "Pan-India",
  "cast": [...],
  "producer_id": "...",
  "status": "pre-production",
  "tag": "current",
  "cast_score": 80.0,
  "historic_score": 70.0,
  "public_pulse_score": 0.0,
  "hws_score": null,
  "created_at": "2026-02-20T...",
  "updated_at": "2026-02-20T..."
}
```

### Update Movie
```
PUT /api/v1/movies/{movie_id}
```

**All fields are optional - only send what you want to update:**

**Example 1: Update Status**
```json
{
  "status": "production"
}
```

**Example 2: Update Release Date**
```json
{
  "release_date": "2027-01-15T00:00:00"
}
```

**Example 3: Update Status and Release Date**
```json
{
  "status": "awaiting-release",
  "release_date": "2027-01-15T00:00:00"
}
```

**Example 4: Update Genres and Languages**
```json
{
  "genres": ["Action", "Thriller"],
  "languages": ["Telugu", "Hindi"]
}
```

**Example 5: Update Cast**
```json
{
  "cast": [
    {"name": "New Actor", "role": "Hero", "star_power": 90},
    {"name": "New Actress", "role": "Heroine", "star_power": 85}
  ]
}
```

### Get Movie Details
```
GET /api/v1/movies/{movie_id}
```

### Get All My Movies
```
GET /api/v1/movies/
```

Returns both current projects and historical movies.

### Delete Movie
```
DELETE /api/v1/movies/{movie_id}
```

## Movie Status Workflow

```
pre-production
    ↓
production
    ↓
post-production
    ↓
awaiting-release
    ↓
released (automatically tagged as "past")
```

## Frontend Integration

### Create Movie Form

```jsx
const [formData, setFormData] = useState({
  title: '',
  director: '',
  genres: [],  // Multiple selection
  languages: [],  // Multiple selection
  budget: '',
  release_date: '',
  region: '',
  status: 'pre-production',
  cast: []
});

// Genre selection (multi-select)
const genreOptions = ['Action', 'Drama', 'Comedy', 'Thriller', 'Romance', 'Horror', 'Sci-Fi'];

// Language selection (multi-select)
const languageOptions = ['Telugu', 'Hindi', 'Tamil', 'Malayalam', 'Kannada', 'English'];

const handleSubmit = async (e) => {
  e.preventDefault();
  try {
    const response = await movieAPI.createMovie(formData);
    console.log('Movie created:', response.data);
  } catch (error) {
    console.error('Failed to create movie:', error);
  }
};
```

### Edit Movie Form

```jsx
const [movie, setMovie] = useState(null);
const [editData, setEditData] = useState({});

// Load movie
useEffect(() => {
  const fetchMovie = async () => {
    const response = await movieAPI.getMovie(movieId);
    setMovie(response.data);
    setEditData({
      status: response.data.status,
      release_date: response.data.release_date,
      genres: response.data.genres,
      languages: response.data.languages
    });
  };
  fetchMovie();
}, [movieId]);

// Update movie
const handleUpdate = async () => {
  try {
    const response = await movieAPI.updateMovie(movieId, editData);
    console.log('Movie updated:', response.data);
  } catch (error) {
    console.error('Failed to update movie:', error);
  }
};

// Status dropdown
<select value={editData.status} onChange={(e) => setEditData({...editData, status: e.target.value})}>
  <option value="pre-production">Pre-Production</option>
  <option value="production">Production</option>
  <option value="post-production">Post-Production</option>
  <option value="awaiting-release">Awaiting Release</option>
  <option value="released">Released</option>
</select>

// Release date picker
<input 
  type="date" 
  value={editData.release_date} 
  onChange={(e) => setEditData({...editData, release_date: e.target.value})}
/>
```

### Multi-Select Component Example

```jsx
import Select from 'react-select';

// Genres multi-select
<Select
  isMulti
  options={genreOptions.map(g => ({ value: g, label: g }))}
  value={formData.genres.map(g => ({ value: g, label: g }))}
  onChange={(selected) => setFormData({
    ...formData, 
    genres: selected.map(s => s.value)
  })}
  placeholder="Select genres..."
/>

// Languages multi-select
<Select
  isMulti
  options={languageOptions.map(l => ({ value: l, label: l }))}
  value={formData.languages.map(l => ({ value: l, label: l }))}
  onChange={(selected) => setFormData({
    ...formData, 
    languages: selected.map(s => s.value)
  })}
  placeholder="Select languages..."
/>
```

## Validation Rules

### Required Fields
- `title` - Movie title
- `director` - Director name
- `genres` - At least one genre
- `languages` - At least one language
- `region` - Region (e.g., "Pan-India", "Telugu States")

### Optional Fields
- `budget` - Budget amount
- `budget_currency` - Default: "INR"
- `release_date` - Expected release date
- `status` - Default: "pre-production"
- `cast` - Array of cast members

### Status Values
- `pre-production`
- `production`
- `post-production`
- `awaiting-release`
- `released`

## Automatic Behaviors

1. **Score Calculation**: When creating/updating a movie:
   - `cast_score` - Calculated from cast members' star power
   - `historic_score` - Calculated from director's past performance and primary genre
   - `public_pulse_score` - Calculated from social media sentiment

2. **Tag Management**:
   - New movies: `tag = "current"`
   - When status changes to "released": `tag = "past"`

3. **Timestamps**:
   - `created_at` - Set on creation
   - `updated_at` - Updated on every edit

## Testing

Run the test script:
```bash
cd backend
python test_movie_crud.py
```

This will test:
- ✅ Movie creation with multiple genres/languages
- ✅ Fetching movie details
- ✅ Updating status
- ✅ Updating release date
- ✅ Updating genres and languages
- ✅ Fetching all movies
- ✅ Deleting movie

## Migration Notes

### Existing Movies
If you have existing movies with old schema:
- `genre` (string) → needs to be converted to `genres` (array)
- `language` (string) → needs to be converted to `languages` (array)
- `themes` → can be removed

### Migration Script (if needed)
```javascript
// In MongoDB
db.movies.updateMany(
  { genre: { $exists: true, $type: "string" } },
  [
    {
      $set: {
        genres: { $cond: [{ $eq: ["$genre", null] }, [], ["$genre"]] },
        languages: { $cond: [{ $eq: ["$language", null] }, [], ["$language"]] }
      }
    },
    {
      $unset: ["genre", "language", "themes"]
    }
  ]
);
```

---

**All changes are backward compatible with proper error handling!** 🎬
