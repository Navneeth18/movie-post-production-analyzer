import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { ArrowLeft, Users, TrendingUp, Calendar, Target, Edit } from 'lucide-react'
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
          <div className="flex items-center space-x-3">
            <span className={`px-4 py-2 rounded-lg text-sm font-medium ${
              movie.status === 'awaiting-release' ? 'bg-orange-100 text-orange-800' :
              movie.status === 'production' ? 'bg-green-100 text-green-800' :
              movie.status === 'post-production' ? 'bg-blue-100 text-blue-800' :
              'bg-gray-100 text-gray-800'
            }`}>
              {movie.status.replace('-', ' ')}
            </span>
            <Link
              to={`/movies/${id}/edit`}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <Edit className="w-4 h-4" />
              <span>Edit</span>
            </Link>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          <div className="space-y-3">
            <div className="flex items-start justify-between py-2 border-b">
              <span className="text-gray-600">Genres</span>
              <div className="flex flex-wrap gap-1 justify-end max-w-xs">
                {(movie.genres || [movie.genre]).map((genre, idx) => (
                  <span key={idx} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                    {genre}
                  </span>
                ))}
              </div>
            </div>
            <div className="flex items-start justify-between py-2 border-b">
              <span className="text-gray-600">Languages</span>
              <div className="flex flex-wrap gap-1 justify-end max-w-xs">
                {(movie.languages || [movie.language]).map((lang, idx) => (
                  <span key={idx} className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium">
                    {lang}
                  </span>
                ))}
              </div>
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
            <div className="flex items-center justify-between py-2 border-b">
              <span className="text-gray-600">Created</span>
              <span className="font-medium text-sm">
                {format(new Date(movie.created_at), 'MMM dd, yyyy')}
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
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
              <h3 className="font-semibold text-gray-900">HWS Score</h3>
            </div>
            <div className="flex items-baseline space-x-2">
              <p className="text-4xl font-bold text-green-600">
                {movie.hws_score?.toFixed(1) || 'N/A'}
              </p>
              {movie.category && (
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                  movie.category === 'BIG' ? 'bg-purple-600 text-white' :
                  movie.category === 'MEDIUM' ? 'bg-blue-600 text-white' :
                  'bg-gray-600 text-white'
                }`}>
                  {movie.category}
                </span>
              )}
            </div>
            <p className="text-sm text-gray-600 mt-1">
              {movie.market_action || 'Historical Weighted Score'}
            </p>
          </div>
        </div>

        {movie.hws_breakdown && (
          <div className="mb-8">
            <h3 className="text-lg font-semibold mb-4">HWS Score Breakdown</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 bg-purple-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Director (25%)</p>
                <p className="text-2xl font-bold text-purple-600">
                  {movie.hws_breakdown.director_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.director_score}
                </p>
              </div>
              <div className="p-4 bg-blue-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Hero (15%)</p>
                <p className="text-2xl font-bold text-blue-600">
                  {movie.hws_breakdown.hero_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.hero_score}
                </p>
              </div>
              <div className="p-4 bg-pink-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Heroine (8%)</p>
                <p className="text-2xl font-bold text-pink-600">
                  {movie.hws_breakdown.heroine_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.heroine_score}
                </p>
              </div>
              <div className="p-4 bg-green-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Genre (20%)</p>
                <p className="text-2xl font-bold text-green-600">
                  {movie.hws_breakdown.genre_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.genre_score}
                </p>
              </div>
              <div className="p-4 bg-yellow-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Popularity (15%)</p>
                <p className="text-2xl font-bold text-yellow-600">
                  {movie.hws_breakdown.popularity_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.popularity_score}
                </p>
              </div>
              <div className="p-4 bg-indigo-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Predicted IMDb (10%)</p>
                <p className="text-2xl font-bold text-indigo-600">
                  {movie.hws_breakdown.predicted_imdb_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.predicted_imdb?.toFixed(0)}
                </p>
              </div>
              <div className="p-4 bg-orange-50 rounded-lg">
                <p className="text-xs text-gray-600 mb-1">Producer (7%)</p>
                <p className="text-2xl font-bold text-orange-600">
                  {movie.hws_breakdown.producer_contribution?.toFixed(1)}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  Score: {movie.hws_breakdown.producer_score}
                </p>
              </div>
            </div>
          </div>
        )}

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

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <Link
            to={`/movies/${id}/public-pulse`}
            className="btn btn-primary"
          >
            Public Pulse Analytics
          </Link>
          <Link
            to={`/movies/${id}/competitors`}
            className="btn btn-secondary"
          >
            Analyze Competitors
          </Link>
          <Link
            to={`/movies/${id}/release-analysis`}
            className="btn btn-secondary"
          >
            Release Strategy
          </Link>
        </div>
      </div>
    </div>
  )
}
