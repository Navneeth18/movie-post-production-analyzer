import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { useAuthStore } from './store/authStore'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Movies from './pages/Movies'
import CreateMovie from './pages/CreateMovie'
import EditMovie from './pages/EditMovie'
import MovieDetail from './pages/MovieDetail'
import PublicPulse from './pages/PublicPulse'
import FacebookCampaign from './pages/FacebookCampaign'
import BudgetPlanning from './pages/BudgetPlanning'
import DataAnalytics from './pages/DataAnalytics'
import CompetitorAnalysis from './pages/CompetitorAnalysis'
import ReleaseDateAnalysis from './pages/ReleaseDateAnalysis'
import Layout from './components/Layout'

function PrivateRoute({ children }) {
  const { token } = useAuthStore()
  return token ? children : <Navigate to="/login" />
}

function App() {
  return (
    <BrowserRouter>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        
        <Route path="/" element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }>
          <Route index element={<Dashboard />} />
          <Route path="movies" element={<Movies />} />
          <Route path="movies/create" element={<CreateMovie />} />
          <Route path="movies/:id" element={<MovieDetail />} />
          <Route path="movies/:id/edit" element={<EditMovie />} />
          <Route path="movies/:id/public-pulse" element={<PublicPulse />} />
          <Route path="movies/:id/facebook-campaign" element={<FacebookCampaign />} />
          <Route path="movies/:id/budget-planning" element={<BudgetPlanning />} />
          <Route path="movies/:id/competitors" element={<CompetitorAnalysis />} />
          <Route path="movies/:id/release-analysis" element={<ReleaseDateAnalysis />} />
          <Route path="analytics" element={<DataAnalytics />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
