# Film Intel Frontend

Modern React frontend for the Film Intelligence Platform.

## Features

- Producer authentication (login/register)
- Movie project management
- Competitor analysis
- Release date strategy
- PR strategy generation
- Real-time score calculations

## Tech Stack

- React 18
- Vite
- Tailwind CSS
- React Router
- Zustand (state management)
- Axios (API calls)
- Lucide React (icons)
- React Hot Toast (notifications)

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment:
```bash
# .env
VITE_API_URL=http://localhost:8000
```

3. Start development server:
```bash
npm run dev
```

The app will run at `http://localhost:5174`

## Project Structure

```
src/
├── components/      # Reusable components
│   └── Layout.jsx   # Main layout with navigation
├── pages/           # Page components
│   ├── Login.jsx
│   ├── Register.jsx
│   ├── Dashboard.jsx
│   ├── Movies.jsx
│   ├── CreateMovie.jsx
│   ├── MovieDetail.jsx
│   ├── CompetitorAnalysis.jsx
│   └── ReleaseDateAnalysis.jsx
├── services/        # API service layer
│   └── api.js
├── store/           # Zustand stores
│   └── authStore.js
├── App.jsx          # Main app component
├── main.jsx         # Entry point
└── index.css        # Global styles
```

## API Integration

All API calls are centralized in `src/services/api.js`:

- `authAPI` - Authentication endpoints
- `movieAPI` - Movie CRUD operations
- `releaseStrategyAPI` - Release strategy analysis

## Features

### Authentication
- Register new producer account
- Login with email/password
- JWT token management
- Auto-redirect on auth failure

### Dashboard
- Overview of all projects
- Quick stats (total, awaiting release, in production)
- Recent projects list

### Movie Management
- Create new movie projects
- View all movies
- Edit movie details
- Delete movies
- Add cast members with star power ratings

### Competitor Analysis
- Compare your movie with competitors
- View cast, historic, and pulse scores
- Get strategic recommendations
- Detect release date conflicts

### Release Strategy
- Analyze competitors in date range
- View big/medium/small movie categories
- Get AI-powered PR strategy
- Receive release date recommendations

## Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Environment Variables

- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)
