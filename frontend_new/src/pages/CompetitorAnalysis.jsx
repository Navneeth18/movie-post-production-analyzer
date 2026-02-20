import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Plus, TrendingUp, AlertCircle } from 'lucide-react'
import { movieAPI } from '../services/api'
import toast from 'react-hot-toast'

export default function CompetitorAnalysis() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [allMovies, setAllMovies] = useState([])
  const [competitors, setCompetitors] = useState([])
  const [selectedCompetitor, setSelectedCompetitor] = useState('')
  const [loading, setLoading] = useState(true)
  const [analyzing, setAnalyzing] = useState(false)

  useEffect(() => {
    loadData()
  }, [id])

  const loadData = async () => {
    try {
      const [movieRes, allMoviesRes, competitorsRes] = await Promise.all([
        movieAPI.getMovie(id),
        movieAPI.getAllMovies('current'),
        movieAPI.getCompetitors(id)
      ])

      setMovie(movieRes.data)
      setAllMovies(allMoviesRes.data.filter(m => m.id !== id))
      setCompetitors(competitorsRes.data)
    } catch (error) {
      toast.error('Failed to load data')
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyze = async () => {
    if (!selectedCompetitor) {
      toast.error('Please select a competitor')
      return
    }

    setAnalyzing(true)
    try {
      await movieAPI.analyzeCompetitor(id, selectedCompetitor)
      toast.success('Competitor analyzed successfully')
      loadData()
      setSelectedCompetitor('')
    } catch (error) {
      toast.error('Failed to analyze competitor')
    } finally {
      setAnalyzing(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
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
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Competitor Analysis</h1>
        <p className="text-gray-600 mb-6">Analyzing: {movie?.title}</p>

        <div className="flex space-x-4 mb-8">
          <select
            value={selectedCompetitor}
            onChange={(e) => setSelectedCompetitor(e.target.value)}
            className="input flex-1"
          >
            <option value="">Select a competitor movie...</option>
            {allMovies.map((m) => (
              <option key={m.id} value={m.id}>
                {m.title} - {m.director} ({m.genre})
              </option>
            ))}
          </select>
          <button
            onClick={handleAnalyze}
            disabled={analyzing || !selectedCompetitor}
            className="btn btn-primary flex items-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>{analyzing ? 'Analyzing...' : 'Analyze'}</span>
          </button>
        </div>

        {competitors.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <AlertCircle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-600">No competitor analyses yet</p>
            <p className="text-sm text-gray-500 mt-2">Select a movie above to start analyzing</p>
          </div>
        ) : (
          <div className="space-y-6">
            {competitors.map((comp, index) => (
              <div key={index} className="card bg-gray-50 border border-gray-200">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{comp.competitor_movie_title}</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      {comp.days_apart} days from your release
                      {comp.release_date_conflict && (
                        <span className="ml-2 px-2 py-1 bg-red-100 text-red-800 text-xs rounded">
                          Date Conflict!
                        </span>
                      )}
                    </p>
                  </div>
                  <span className={`px-4 py-2 rounded-lg text-sm font-medium ${
                    comp.overall_strength === 'stronger' ? 'bg-green-100 text-green-800' :
                    comp.overall_strength === 'weaker' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    You are {comp.overall_strength}
                  </span>
                </div>

                <div className="grid grid-cols-3 gap-4 mb-4">
                  <div className="text-center p-3 bg-white rounded">
                    <p className="text-xs text-gray-600 mb-1">Cast Score</p>
                    <div className="flex items-center justify-center space-x-2">
                      <span className="text-lg font-bold text-blue-600">{comp.your_cast_score.toFixed(0)}</span>
                      <span className="text-gray-400">vs</span>
                      <span className="text-lg font-bold text-gray-600">{comp.competitor_cast_score.toFixed(0)}</span>
                    </div>
                  </div>

                  <div className="text-center p-3 bg-white rounded">
                    <p className="text-xs text-gray-600 mb-1">Historic Score</p>
                    <div className="flex items-center justify-center space-x-2">
                      <span className="text-lg font-bold text-green-600">{comp.your_historic_score.toFixed(0)}</span>
                      <span className="text-gray-400">vs</span>
                      <span className="text-lg font-bold text-gray-600">{comp.competitor_historic_score.toFixed(0)}</span>
                    </div>
                  </div>

                  <div className="text-center p-3 bg-white rounded">
                    <p className="text-xs text-gray-600 mb-1">Pulse Score</p>
                    <div className="flex items-center justify-center space-x-2">
                      <span className="text-lg font-bold text-purple-600">{comp.your_pulse_score.toFixed(0)}</span>
                      <span className="text-gray-400">vs</span>
                      <span className="text-lg font-bold text-gray-600">{comp.competitor_pulse_score.toFixed(0)}</span>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start space-x-2">
                    <TrendingUp className="w-5 h-5 text-blue-600 mt-0.5" />
                    <div>
                      <p className="font-medium text-gray-900 mb-1">Recommendation</p>
                      <p className="text-sm text-gray-700">{comp.recommendation}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
