import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Calendar, AlertTriangle, CheckCircle, Film } from 'lucide-react'
import { movieAPI, releaseStrategyAPI } from '../services/api'
import toast from 'react-hot-toast'
import { format } from 'date-fns'

export default function ReleaseDateAnalysis() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)
  const [dateRange, setDateRange] = useState({ days_before: 30, days_after: 30 })

  useEffect(() => {
    loadMovie()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await movieAPI.getMovie(id)
      setMovie(data)
    } catch (error) {
      toast.error('Failed to load movie')
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyze = async () => {
    if (!movie.release_date) {
      toast.error('Please set a release date for your movie first')
      return
    }

    setAnalyzing(true)
    try {
      const { data } = await releaseStrategyAPI.analyzeDateRange({
        movie_id: id,
        target_release_date: movie.release_date,
        days_before: dateRange.days_before,
        days_after: dateRange.days_after
      })
      setAnalysis(data)
      toast.success('Analysis complete')
    } catch (error) {
      toast.error('Failed to analyze release date')
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  const getCategoryColor = (category) => {
    switch (category) {
      case 'big': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-orange-100 text-orange-800'
      case 'small': return 'bg-blue-100 text-blue-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getThreatColor = (threat) => {
    switch (threat) {
      case 'high': return 'bg-red-100 text-red-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'low': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="max-w-6xl mx-auto space-y-6">
      <button
        onClick={() => navigate(`/movies/${id}`)}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movie</span>
      </button>

      <div className="card">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Release Date Analysis</h1>
        <p className="text-gray-600 mb-6">{movie?.title}</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="label">Days Before</label>
            <input
              type="number"
              value={dateRange.days_before}
              onChange={(e) => setDateRange({...dateRange, days_before: parseInt(e.target.value)})}
              className="input"
              min="7"
              max="90"
            />
          </div>
          <div>
            <label className="label">Days After</label>
            <input
              type="number"
              value={dateRange.days_after}
              onChange={(e) => setDateRange({...dateRange, days_after: parseInt(e.target.value)})}
              className="input"
              min="7"
              max="90"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={handleAnalyze}
              disabled={analyzing || !movie?.release_date}
              className="btn btn-primary w-full"
            >
              {analyzing ? 'Analyzing...' : 'Analyze Date Range'}
            </button>
          </div>
        </div>

        {!movie?.release_date && (
          <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <div className="flex items-start space-x-2">
              <AlertTriangle className="w-5 h-5 text-yellow-600 mt-0.5" />
              <p className="text-sm text-yellow-800">
                Please set a release date for your movie to perform analysis
              </p>
            </div>
          </div>
        )}

        {analysis && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="card bg-blue-50 border border-blue-200">
                <p className="text-sm text-gray-600 mb-1">Total Competitors</p>
                <p className="text-3xl font-bold text-blue-600">{analysis.total_competitors}</p>
              </div>
              <div className="card bg-red-50 border border-red-200">
                <p className="text-sm text-gray-600 mb-1">Big Movies</p>
                <p className="text-3xl font-bold text-red-600">{analysis.big_movies_count}</p>
              </div>
              <div className="card bg-orange-50 border border-orange-200">
                <p className="text-sm text-gray-600 mb-1">Medium Movies</p>
                <p className="text-3xl font-bold text-orange-600">{analysis.medium_movies_count}</p>
              </div>
              <div className="card bg-purple-50 border border-purple-200">
                <p className="text-sm text-gray-600 mb-1">High Threats</p>
                <p className="text-3xl font-bold text-purple-600">{analysis.high_threat_count}</p>
              </div>
            </div>

            <div className={`card ${
              analysis.risk_assessment.includes('HIGH') ? 'bg-red-50 border-red-200' :
              analysis.risk_assessment.includes('MEDIUM') ? 'bg-yellow-50 border-yellow-200' :
              'bg-green-50 border-green-200'
            } border`}>
              <div className="flex items-start space-x-3">
                {analysis.risk_assessment.includes('HIGH') ? (
                  <AlertTriangle className="w-6 h-6 text-red-600 mt-1" />
                ) : (
                  <CheckCircle className="w-6 h-6 text-green-600 mt-1" />
                )}
                <div>
                  <h3 className="font-semibold text-gray-900 mb-2">Risk Assessment</h3>
                  <p className="text-gray-700">{analysis.risk_assessment}</p>
                  <p className="text-gray-700 mt-2">{analysis.recommendation}</p>
                </div>
              </div>
            </div>

            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Competitors in Date Range</h3>
              <div className="space-y-3">
                {analysis.competitors.map((comp, index) => (
                  <div key={index} className="p-4 border border-gray-200 rounded-lg hover:border-blue-500 transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h4 className="font-semibold text-gray-900">{comp.title}</h4>
                        <p className="text-sm text-gray-600">{comp.director} • {comp.genre}</p>
                      </div>
                      <div className="flex space-x-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getCategoryColor(comp.category)}`}>
                          {comp.category}
                        </span>
                        <span className={`px-2 py-1 rounded text-xs font-medium ${getThreatColor(comp.threat_level)}`}>
                          {comp.threat_level} threat
                        </span>
                      </div>
                    </div>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-sm">
                      <div>
                        <p className="text-gray-600">Release Date</p>
                        <p className="font-medium">{format(new Date(comp.release_date), 'MMM dd, yyyy')}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Days Apart</p>
                        <p className="font-medium">{comp.days_from_your_release} days</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Budget</p>
                        <p className="font-medium">₹{(comp.budget / 10000000).toFixed(1)}Cr</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Language</p>
                        <p className="font-medium">{comp.language}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
