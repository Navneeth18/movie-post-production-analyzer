import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Film, TrendingUp, Users, Calendar } from 'lucide-react'
import { movieAPI } from '../services/api'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [movies, setMovies] = useState([])
  const [stats, setStats] = useState({
    total: 0,
    awaiting: 0,
    production: 0,
    avgScore: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboard()
  }, [])

  const loadDashboard = async () => {
    try {
      const { data } = await movieAPI.getMyMovies()
      setMovies(data)
      
      // Calculate stats
      const awaiting = data.filter(m => m.status === 'awaiting-release').length
      const production = data.filter(m => m.status === 'production').length
      const avgScore = data.length > 0 
        ? data.reduce((sum, m) => sum + (m.cast_score || 0), 0) / data.length 
        : 0

      setStats({
        total: data.length,
        awaiting,
        production,
        avgScore: avgScore.toFixed(1)
      })
    } catch (error) {
      toast.error('Failed to load dashboard')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">Welcome back! Here's your project overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Projects</p>
              <p className="text-3xl font-bold text-gray-900 mt-1">{stats.total}</p>
            </div>
            <Film className="w-12 h-12 text-blue-600 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Awaiting Release</p>
              <p className="text-3xl font-bold text-orange-600 mt-1">{stats.awaiting}</p>
            </div>
            <Calendar className="w-12 h-12 text-orange-600 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">In Production</p>
              <p className="text-3xl font-bold text-green-600 mt-1">{stats.production}</p>
            </div>
            <TrendingUp className="w-12 h-12 text-green-600 opacity-20" />
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Avg Cast Score</p>
              <p className="text-3xl font-bold text-purple-600 mt-1">{stats.avgScore}</p>
            </div>
            <Users className="w-12 h-12 text-purple-600 opacity-20" />
          </div>
        </div>
      </div>

      {/* Recent Projects */}
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900">Recent Projects</h2>
          <Link to="/movies" className="text-blue-600 hover:underline text-sm">
            View all
          </Link>
        </div>

        {movies.length === 0 ? (
          <div className="text-center py-12">
            <Film className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600 mb-4">No projects yet</p>
            <Link to="/movies/create" className="btn btn-primary">
              Create Your First Project
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {movies.slice(0, 5).map((movie) => (
              <Link
                key={movie.id}
                to={`/movies/${movie.id}`}
                className="block p-4 border border-gray-200 rounded-lg hover:border-blue-500 hover:shadow-md transition-all"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-semibold text-gray-900">{movie.title}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {movie.genre} • {movie.language} • {movie.director}
                    </p>
                  </div>
                  <div className="text-right">
                    <span className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                      movie.status === 'awaiting-release' ? 'bg-orange-100 text-orange-800' :
                      movie.status === 'production' ? 'bg-green-100 text-green-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {movie.status}
                    </span>
                    <p className="text-sm text-gray-600 mt-2">
                      Cast Score: <span className="font-semibold">{movie.cast_score?.toFixed(1) || 'N/A'}</span>
                    </p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
