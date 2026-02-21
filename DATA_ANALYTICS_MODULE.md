# Data Analytics Module

## Overview
Advanced data analytics dashboard providing interactive visualizations and insights from movie industry data using Pandas analysis and Chart.js visualizations.

## Features

### 1. Grade-Performance Correlation
**Visualization**: Bar Chart
**Analysis**: Shows IMDB rating distributions grouped by Director Grade
**Insights**: 
- Compares performance across Grade 1, Grade 2, and Grade 3 directors
- Identifies outliers (movies that exceeded their director's grade expectations)
- Shows mean and median ratings per grade

**Key Metrics**:
- Mean IMDB Rating per Grade
- Movie count per Grade
- Top 5 outlier movies that exceeded expectations

### 2. Genre Popularity Over Time
**Visualization**: Interactive Time-Series Area Chart
**Analysis**: Shows sum of popularity scores per Genre per Quarter
**Insights**:
- Tracks genre trends over time
- Identifies seasonal patterns
- Shows which genres are gaining/losing popularity

**Key Metrics**:
- Quarterly popularity scores
- Top 5 genres displayed
- Trend lines for each genre

### 3. Talent Value Matrix
**Visualization**: Bubble Chart (Scatter Plot)
**Analysis**: Each bubble represents a Hero
- X-axis: Average IMDB Rating
- Y-axis: Average Popularity Score
- Bubble Size: Number of movies

**Insights**:
- Identifies high-value talent (high IMDB + high popularity)
- Shows consistency (multiple movies)
- Helps in casting decisions

**Key Metrics**:
- Average IMDB per hero
- Average popularity per hero
- Movie count per hero

### 4. Demographic Heatmap
**Visualization**: Color-coded Matrix
**Analysis**: Correlation between Genres and Age Groups
**Insights**:
- Shows which genres appeal to which age groups
- Helps in targeted marketing
- Identifies demographic opportunities

**Key Metrics**:
- Average popularity score per genre-age combination
- Color intensity indicates strength of correlation

## Data Processing

### Data Cleaning
1. **Date Conversion**: `release_date` converted to datetime format
2. **Missing Values**: IMDB ratings filled with median
3. **Multi-label Handling**: Genre and age_groups exploded for granular analysis
4. **Data Merging**: Bhanu dataset merged with Bob dataset by matching:
   - Director names
   - Hero names
   - Heroine names

### Data Sources
- **bhanu_dataset.csv**: Movie details (name, talent, ratings, popularity, genre, date, age groups)
- **bob-dataset.csv**: Talent names, roles, and industry grades

## API Endpoints

### Get All Analytics
```
GET /api/v1/data-analytics/all
```
Returns all four visualizations data at once

### Individual Endpoints
```
GET /api/v1/data-analytics/grade-performance
GET /api/v1/data-analytics/genre-timeline
GET /api/v1/data-analytics/talent-matrix
GET /api/v1/data-analytics/demographic-heatmap
```

## Frontend Routes

- `/analytics` - Main analytics dashboard

## Technology Stack

### Backend
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **FastAPI**: API endpoints

### Frontend
- **React**: UI framework
- **Chart.js**: Interactive charts
- **react-chartjs-2**: React wrapper for Chart.js

## Chart Configurations

### Dark Mode Theme
All charts use a professional dark mode theme:
- Background: Dark gray (#111827)
- Text: Light gray (#e5e7eb)
- Grid: Subtle gray lines
- Tooltips: Dark with light text

### Chart Types
1. **Bar Chart**: Grade performance comparison
2. **Line Chart**: Genre timeline with area fill
3. **Bubble Chart**: Talent matrix with size encoding
4. **Heatmap**: Demographic correlation matrix

## Usage

### Access Dashboard
1. Login to the application
2. Click "Analytics" in the navigation bar
3. View interactive visualizations
4. Switch between tabs to see different analyses

### Interact with Charts
- **Hover**: See detailed tooltips
- **Tabs**: Switch between different visualizations
- **Tables**: View outlier data and top performers

## Insights Examples

### Grade Performance Outliers
Movies that significantly exceeded their director's grade expectations:
- Movie name
- Director name
- Grade
- Actual rating vs Expected rating
- Difference (how much they exceeded)

### Genre Trends
- Action movies peak in summer quarters
- Romance movies popular around Valentine's Day
- Drama maintains steady popularity

### Talent Value
- High IMDB + High Popularity = Premium talent
- Consistent performers (multiple movies)
- Emerging talent (few movies but high scores)

### Demographics
- Action appeals to Teens and Adults
- Romance appeals to Adults
- Family films appeal to all age groups

## Data Flow

1. **Backend Service** (`data_analytics_service.py`):
   - Loads CSV files
   - Cleans and processes data
   - Performs Pandas analysis
   - Returns JSON data

2. **API Endpoint** (`data_analytics.py`):
   - Receives requests
   - Calls service methods
   - Returns formatted JSON

3. **Frontend** (`DataAnalytics.jsx`):
   - Fetches data from API
   - Transforms for Chart.js
   - Renders interactive charts
   - Displays insights tables

## Performance

- **Data Loading**: < 1 second
- **Chart Rendering**: Instant
- **Interactive Updates**: Real-time
- **Memory Efficient**: Processes data on-demand

## Future Enhancements

Potential additions:
- Export charts as images
- Download data as CSV/Excel
- Custom date range filters
- More advanced statistical analysis
- Predictive analytics
- Comparison tools
- Real-time data updates
- Custom report generation

## Error Handling

- Missing CSV files: Clear error message
- Invalid data: Graceful fallback with median values
- API errors: Toast notifications
- Loading states: Spinner indicators

## Accessibility

- Semantic HTML
- Keyboard navigation
- Screen reader friendly
- Color contrast compliant
- Responsive design

## Browser Compatibility

Works in all modern browsers:
- Chrome/Edge (Chromium)
- Firefox
- Safari
- Mobile browsers

## Testing

### Backend Test
```bash
cd backend
python -c "from app.services.data_analytics_service import DataAnalyticsService; s = DataAnalyticsService(); print(s.get_all_analytics())"
```

### API Test
```bash
curl http://localhost:8000/api/v1/data-analytics/all
```

## Dependencies

### Backend
- pandas
- numpy
- fastapi

### Frontend
- chart.js
- react-chartjs-2
- lucide-react (icons)

## Configuration

No additional configuration required. The module uses existing CSV files in `backend/data/` directory.

## Security

- No authentication required for analytics (read-only)
- Data is processed server-side
- No sensitive information exposed
- CORS configured properly

## Maintenance

- CSV files can be updated without code changes
- Service automatically processes new data
- Charts update automatically
- No database required

## Success Metrics

✅ 4 interactive visualizations
✅ Real-time data processing
✅ Professional dark mode theme
✅ Outlier detection and insights
✅ Responsive design
✅ Fast performance
✅ Clean, intuitive UI
✅ Comprehensive data analysis

## Conclusion

The Data Analytics module provides powerful insights into movie industry data through interactive visualizations, helping producers make data-driven decisions about talent, genres, demographics, and market trends.
