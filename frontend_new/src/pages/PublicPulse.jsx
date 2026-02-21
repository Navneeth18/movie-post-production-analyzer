import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, TrendingUp, ThumbsUp, ThumbsDown, Eye, MessageCircle, RefreshCw, Youtube, BarChart3 } from 'lucide-react'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import toast from 'react-hot-toast'
import api from '../services/api'

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default function PublicPulse() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [movie, setMovie] = useState(null)
  const [pulseData, setPulseData] = useState(null)
  const [history, setHistory] = useState([])
  const [youtubeUrl, setYoutubeUrl] = useState('')
  const [addingTrailer, setAddingTrailer] = useState(false)

  useEffect(() => {
    loadMovie()
    loadPulseData()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await api.get(`/movies/${id}`)
      setMovie(data)
    } catch (error) {
      toast.error('Failed to load movie')
      navigate('/movies')
    }
  }

  const loadPulseData = async () => {
    try {
      // Try to load current pulse data
      const { data: current } = await api.get(`/public-pulse/${id}/current`)
      setPulseData(current)

      // Load history for graph
      const { data: historyData } = await api.get(`/public-pulse/${id}/history`)
      setHistory(historyData)
    } catch (error) {
      // No pulse data yet
      setPulseData(null)
      setHistory([])
    } finally {
      setLoading(false)
    }
  }

  const handleAddTrailer = async (e) => {
    e.preventDefault()
    if (!youtubeUrl) {
      toast.error('Please enter a YouTube URL')
      return
    }

    setAddingTrailer(true)
    try {
      await api.post(`/public-pulse/${id}/add-trailer`, {
        youtube_url: youtubeUrl
      })
      toast.success('Trailer added successfully!')
      setYoutubeUrl('')
      await loadMovie()
      await loadPulseData()
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to add trailer')
    } finally {
      setAddingTrailer(false)
    }
  }

  const handleRefreshPulse = async () => {
    setRefreshing(true)
    try {
      await api.post(`/public-pulse/${id}/refresh-pulse`)
      toast.success('Public pulse refreshed!')
      await loadPulseData()
    } catch (error) {
      toast.error('Failed to refresh pulse data')
    } finally {
      setRefreshing(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  // Prepare chart data
  const chartData = {
    labels: history.map(h => new Date(h.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Public Pulse Score',
        data: history.map(h => h.pulse_score),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        fill: true,
        tension: 0.4
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        display: false
      },
      title: {
        display: true,
        text: 'Public Pulse Over Time'
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        title: {
          display: true,
          text: 'Pulse Score'
        }
      }
    }
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment) {
      case 'Positive': return 'text-green-600 bg-green-100'
      case 'Negative': return 'text-red-600 bg-red-100'
      default: return 'text-gray-600 bg-gray-100'
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
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Public Pulse Analytics</h1>
            <p className="text-gray-600 mt-2">{movie?.title}</p>
          </div>
          {pulseData && (
            <button
              onClick={handleRefreshPulse}
              disabled={refreshing}
              className="btn btn-secondary flex items-center space-x-2"
            >
              <RefreshCw className={`w-4 h-4 ${refreshing ? 'animate-spin' : ''}`} />
              <span>{refreshing ? 'Refreshing...' : 'Refresh Data'}</span>
            </button>
          )}
        </div>

        {!pulseData ? (
          <div className="text-center py-12">
            <Youtube className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No Trailer Linked</h3>
            <p className="text-gray-600 mb-6">Add a YouTube trailer to start tracking public pulse</p>

            <form onSubmit={handleAddTrailer} className="max-w-md mx-auto">
              <div className="flex space-x-2">
                <input
                  type="url"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="input flex-1"
                  required
                />
                <button
                  type="submit"
                  disabled={addingTrailer}
                  className="btn btn-primary"
                >
                  {addingTrailer ? 'Adding...' : 'Add Trailer'}
                </button>
              </div>
              <p className="text-xs text-gray-500 mt-2">
                Paste the full YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
              </p>
            </form>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Change Trailer Section */}
            <div className="card bg-gray-50">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">Change Trailer</h3>
              <form onSubmit={handleAddTrailer} className="flex space-x-2">
                <input
                  type="url"
                  value={youtubeUrl}
                  onChange={(e) => setYoutubeUrl(e.target.value)}
                  placeholder="https://www.youtube.com/watch?v=..."
                  className="input flex-1"
                />
                <button
                  type="submit"
                  disabled={addingTrailer}
                  className="btn btn-secondary"
                >
                  {addingTrailer ? 'Updating...' : 'Update Trailer'}
                </button>
              </form>
              <p className="text-xs text-gray-500 mt-2">
                Current video ID: {pulseData.youtube_video_id}
              </p>
            </div>

            {/* Current Pulse Score */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <div className="card bg-blue-50 border border-blue-200">
                <div className="flex items-center space-x-3 mb-2">
                  <TrendingUp className="w-6 h-6 text-blue-600" />
                  <h3 className="font-semibold text-gray-900">Pulse Score</h3>
                </div>
                <p className="text-4xl font-bold text-blue-600">
                  {pulseData.current_pulse_score.toFixed(1)}
                </p>
                <span className={`inline-block px-2 py-1 rounded text-xs font-medium mt-2 ${getSentimentColor(pulseData.sentiment)}`}>
                  {pulseData.sentiment}
                </span>
              </div>

              <div className="card bg-green-50 border border-green-200">
                <div className="flex items-center space-x-3 mb-2">
                  <ThumbsUp className="w-6 h-6 text-green-600" />
                  <h3 className="font-semibold text-gray-900">Likes</h3>
                </div>
                <p className="text-4xl font-bold text-green-600">
                  {pulseData.likes.toLocaleString()}
                </p>
              </div>

              <div className="card bg-purple-50 border border-purple-200">
                <div className="flex items-center space-x-3 mb-2">
                  <Eye className="w-6 h-6 text-purple-600" />
                  <h3 className="font-semibold text-gray-900">Views</h3>
                </div>
                <p className="text-4xl font-bold text-purple-600">
                  {pulseData.views.toLocaleString()}
                </p>
              </div>

              <div className="card bg-orange-50 border border-orange-200">
                <div className="flex items-center space-x-3 mb-2">
                  <BarChart3 className="w-6 h-6 text-orange-600" />
                  <h3 className="font-semibold text-gray-900">Engagement</h3>
                </div>
                <p className="text-4xl font-bold text-orange-600">
                  {pulseData.engagement_rate.toFixed(2)}%
                </p>
              </div>
            </div>

            {/* YouTube Video Embed */}
            <div className="card">
              <h3 className="text-lg font-semibold mb-4">Trailer</h3>
              <div className="aspect-video">
                <iframe
                  width="100%"
                  height="100%"
                  src={`https://www.youtube.com/embed/${pulseData.youtube_video_id}`}
                  title="YouTube video player"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                  className="rounded-lg"
                ></iframe>
              </div>
            </div>

            {/* Pulse History Graph */}
            {history.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">Pulse Trend</h3>
                <Line data={chartData} options={chartOptions} />
              </div>
            )}

            {/* History Table */}
            {history.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold mb-4">History</h3>
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Pulse Score</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Likes</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Views</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Comments</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {history.map((h, idx) => (
                        <tr key={idx}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {new Date(h.date).toLocaleDateString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                            {h.pulse_score.toFixed(1)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {h.likes.toLocaleString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {h.views.toLocaleString()}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {h.comments_analyzed}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
