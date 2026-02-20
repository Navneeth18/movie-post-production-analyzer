import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, Users, TrendingUp, Calendar, Target } from 'lucide-react'
import { movieAPI } from '../services/api'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function MovieDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadMovie()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await movieAPI.getMovie(id)
      setMovie(data)
    } catch (error) {
      toast.error('Failed to load movie')
      navigate('/movies')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!movie) {
    return <div className="text-center py-12">Movie not found</div>
  }

  const category = movie.budget >= 50000000 ? 'Big' : 
                   movie.budget >= 15000000 ? 'Medium' : 'Small'

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <button
        onClick={() => navigate('/movies')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movies</span>
      </button>

      <div className="card">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">{movie.title}</h1>
            <p className="text-gray-600 mt-2">Directed by {movie.director}</p>
          </div>
          <span className={`px-4 py-2 rounded-lg text-sm font-medium ${
            movie.status === 'awaiting-release' ? 'bg-orange-100 text-orange-800' :
            movie.status === 'production' ? 'bg-green-100 text-green-800' :
            'bg-gray-100 text-gray-800'
          }`}>
            {movie.status}
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Genre</span>
              <span className="font-medium">{movie.genre}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Language</span>
              <span className="font-medium">{movie.language}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Region</span>
              <span className="font-medium">{movie.region}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Budget</span>
              <span className="font-medium">₹{(movie.budget / 10000000).toFixed(2)} Cr</span>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Category</span>
              <span className={`font-medium ${
                category === 'Big' ? 'text-red-600' :
                category === 'Medium' ? 'text-orange-600' :
                'text-blue-600'
              }`}>{category} Movie</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Release Date</span>
              <span className="font-medium">
                {movie.release_date ? format(new Date(movie.release_date), 'MMM dd, yyyy') : 'Not set'}
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Tag</span>
              <span className={`px-2 py-1 rounded text-xs font-medium ${
                movie.tag === 'current' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {movie.tag}
              </span>
            </div>
          </div>
        </div>

        {movie.themes && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-2">Themes</h3>
            <p className="text-gray-700">{movie.themes}</p>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card bg-blue-50 border border-blue-200">
            <div className="flex items-center space-x-3 mb-2">
              <Users className="w-6 h-6 text-blue-600" />
              <h3 className="font-semibold text-gray-900">Cast Score</h3>
            </div>
            <p className="text-4xl font-bold text-blue-600">
              {movie.cast_score?.toFixed(1) || 'N/A'}
            </p>
            <p className="text-sm text-gray-600 mt-1">Star power rating</p>
          </div>

          <div className="card bg-green-50 border border-green-200">
            <div className="flex items-center space-x-3 mb-2">
              <TrendingUp className="w-6 h-6 text-green-600" />
              <h3 className="font-semibold text-gray-900">Historic Score</h3>
            </div>
            <p className="text-4xl font-bold text-green-600">
              {movie.historic_score?.toFixed(1) || 'N/A'}
            </p>
            <p className="text-sm text-gray-600 mt-1">Director & genre performance</p>
          </div>

          <div className="card bg-purple-50 border border-purple-200">
            <div className="flex items-center space-x-3 mb-2">
              <Target className="w-6 h-6 text-purple-600" />
              <h3 className="font-semibold text-gray-900">Public Pulse</h3>
            </div>
            <p className="text-4xl font-bold text-purple-600">
              {movie.public_pulse_score?.toFixed(1) || 'N/A'}
            </p>
            <p className="text-sm text-gray-600 mt-1">Social sentiment</p>
          </div>
        </div>

        {movie.cast && movie.cast.length > 0 && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">Cast Members</h3>
            <div className="space-y-2">
              {movie.cast.map((member, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div>
                    <span className="font-medium">{member.name}</span>
                    <span className="text-gray-600"> as {member.role}</span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Star Power: </span>
                    <span className="font-semibold text-blue-600">{member.star_power || 50}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex space-x-4">
          <Link
            to={`/movies/${id}/competitors`}
            className="btn btn-primary flex-1"
          >
            Analyze Competitors
          </Link>
          <Link
            to={`/movies/${id}/release-analysis`}
            className="btn btn-secondary flex-1"
          >
            Release Strategy
          </Link>
        </div>
      </div>
    </div>
  )
}
