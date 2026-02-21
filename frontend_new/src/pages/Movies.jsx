import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Film, Plus, Trash2, Eye } from 'lucide-react'
import { movieAPI } from '../services/api'
import toast from 'react-hot-toast'

export default function Movies() {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMovies()
  }, [])

  const loadMovies = async () => {
    try {
      const { data } = await movieAPI.getMyMovies()
      setMovies(data)
    } catch (error) {
      toast.error('Failed to load movies')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this movie?')) return

    try {
      await movieAPI.deleteMovie(id)
      toast.success('Movie deleted')
      loadMovies()
    } catch (error) {
      toast.error('Failed to delete movie')
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Movies</h1>
          <p className="text-gray-600 mt-2">Manage your film projects</p>
        </div>
        <Link to="/movies/create" className="btn btn-primary flex items-center space-x-2">
          <Plus className="w-5 h-5" />
          <span>New Project</span>
        </Link>
      </div>

      {movies.length === 0 ? (
        <div className="card text-center py-12">
          <Film className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-600 mb-4">No movies yet</p>
          <Link to="/movies/create" className="btn btn-primary">
            Create Your First Project
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {movies.map((movie) => (
            <div key={movie.id} className="card hover:shadow-lg transition-shadow">
              <div className="mb-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-xl font-bold text-gray-900">{movie.title}</h3>
                  <span className={`px-2 py-1 rounded text-xs font-medium ${
                    movie.status === 'awaiting-release' ? 'bg-orange-100 text-orange-800' :
                    movie.status === 'production' ? 'bg-green-100 text-green-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {movie.status}
                  </span>
                </div>
                {movie.category && (
                  <span className={`inline-block px-3 py-1 rounded-full text-xs font-bold ${
                    movie.category === 'BIG' ? 'bg-purple-100 text-purple-800' :
                    movie.category === 'MEDIUM' ? 'bg-blue-100 text-blue-800' :
                    'bg-gray-100 text-gray-800'
                  }`}>
                    {movie.category} MOVIE
                  </span>
                )}
              </div>

              <div className="space-y-2 text-sm text-gray-600 mb-4">
                <p><span className="font-medium">Director:</span> {movie.director}</p>
                <div>
                  <span className="font-medium">Genres:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {(movie.genres || [movie.genre]).slice(0, 3).map((genre, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs">
                        {genre}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <span className="font-medium">Languages:</span>
                  <div className="flex flex-wrap gap-1 mt-1">
                    {(movie.languages || [movie.language]).slice(0, 3).map((lang, idx) => (
                      <span key={idx} className="px-2 py-0.5 bg-green-100 text-green-800 rounded text-xs">
                        {lang}
                      </span>
                    ))}
                  </div>
                </div>
                <p><span className="font-medium">Budget:</span> ₹{(movie.budget / 10000000).toFixed(2)}Cr</p>
              </div>

              <div className="grid grid-cols-2 gap-2 mb-4 text-center">
                <div className="bg-blue-50 p-2 rounded">
                  <p className="text-xs text-gray-600">Cast</p>
                  <p className="text-lg font-bold text-blue-600">{movie.cast_score?.toFixed(0) || 'N/A'}</p>
                </div>
                <div className="bg-green-50 p-2 rounded">
                  <p className="text-xs text-gray-600">HWS</p>
                  <p className="text-lg font-bold text-green-600">{movie.hws_score?.toFixed(0) || 'N/A'}</p>
                </div>
              </div>

              <div className="flex space-x-2">
                <Link
                  to={`/movies/${movie.id}`}
                  className="flex-1 btn btn-secondary flex items-center justify-center space-x-1"
                >
                  <Eye className="w-4 h-4" />
                  <span>View</span>
                </Link>
                <button
                  onClick={() => handleDelete(movie.id)}
                  className="btn btn-danger flex items-center space-x-1"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
