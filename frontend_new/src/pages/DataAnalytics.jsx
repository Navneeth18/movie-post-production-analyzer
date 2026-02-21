import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { BarChart3, TrendingUp, Users, Target } from 'lucide-react'
import { dataAnalyticsAPI } from '../services/api'
import toast from 'react-hot-toast'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar, Scatter, Bubble } from 'react-chartjs-2'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

export default function DataAnalytics() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [analytics, setAnalytics] = useState(null)
  const [activeTab, setActiveTab] = useState('grade')

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      const { data } = await dataAnalyticsAPI.getAllAnalytics()
      setAnalytics(data)
    } catch (error) {
      toast.error('Failed to load analytics data')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  if (!analytics) {
    return <div className="text-center py-12">No analytics data available</div>
  }

  // Chart configurations with dark theme
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: {
          color: '#e5e7eb',
          font: { size: 12 }
        }
      },
      tooltip: {
        backgroundColor: 'rgba(17, 24, 39, 0.95)',
        titleColor: '#f3f4f6',
        bodyColor: '#e5e7eb',
        borderColor: '#374151',
        borderWidth: 1
      }
    },
    scales: {
      x: {
        ticks: { color: '#9ca3af' },
        grid: { color: 'rgba(75, 85, 99, 0.2)' }
      },
      y: {
        ticks: { color: '#9ca3af' },
        grid: { color: 'rgba(75, 85, 99, 0.2)' }
      }
    }
  }

  // Grade Performance Chart Data
  const gradePerformanceData = {
    labels: analytics.grade_performance.data.map(d => d.grade),
    datasets: [{
      label: 'Mean IMDB Rating',
      data: analytics.grade_performance.data.map(d => d.mean),
      backgroundColor: 'rgba(59, 130, 246, 0.7)',
      borderColor: 'rgb(59, 130, 246)',
      borderWidth: 2
    }]
  }

  // Genre Timeline Chart Data
  const genreTimelineData = {
    labels: analytics.genre_timeline.data.map(d => d.quarter),
    datasets: analytics.genre_timeline.genres.slice(0, 5).map((genre, index) => {
      const colors = [
        'rgba(59, 130, 246, 0.6)',
        'rgba(16, 185, 129, 0.6)',
        'rgba(245, 158, 11, 0.6)',
        'rgba(239, 68, 68, 0.6)',
        'rgba(139, 92, 246, 0.6)'
      ]
      return {
        label: genre,
        data: analytics.genre_timeline.data.map(d => d[genre] || 0),
        backgroundColor: colors[index],
        borderColor: colors[index].replace('0.6', '1'),
        borderWidth: 2,
        fill: true
      }
    })
  }

  // Talent Matrix Chart Data
  const talentMatrixData = {
    datasets: [{
      label: 'Heroes',
      data: analytics.talent_matrix.data.map(d => ({
        x: d.avg_imdb,
        y: d.avg_popularity,
        r: Math.sqrt(d.movie_count) * 5,
        hero: d.hero,
        count: d.movie_count
      })),
      backgroundColor: 'rgba(59, 130, 246, 0.6)',
      borderColor: 'rgb(59, 130, 246)',
      borderWidth: 2
    }]
  }

  const talentMatrixOptions = {
    ...chartOptions,
    plugins: {
      ...chartOptions.plugins,
      tooltip: {
        ...chartOptions.plugins.tooltip,
        callbacks: {
          label: (context) => {
            const point = context.raw
            return [
              `Hero: ${point.hero}`,
              `Avg IMDB: ${point.x.toFixed(2)}`,
              `Avg Popularity: ${point.y.toFixed(2)}`,
              `Movies: ${point.count}`
            ]
          }
        }
      }
    },
    scales: {
      x: {
        ...chartOptions.scales.x,
        title: { display: true, text: 'Average IMDB Rating', color: '#9ca3af' }
      },
      y: {
        ...chartOptions.scales.y,
        title: { display: true, text: 'Average Popularity Score', color: '#9ca3af' }
      }
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="card">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Data Analytics Dashboard</h1>
        <p className="text-gray-600">Advanced insights from movie industry data</p>
      </div>

      {/* Tab Navigation */}
      <div className="card">
        <div className="flex space-x-2 overflow-x-auto">
          <button
            onClick={() => setActiveTab('grade')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'grade'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <BarChart3 className="w-4 h-4 inline mr-2" />
            Grade Performance
          </button>
          <button
            onClick={() => setActiveTab('timeline')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'timeline'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <TrendingUp className="w-4 h-4 inline mr-2" />
            Genre Timeline
          </button>
          <button
            onClick={() => setActiveTab('talent')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'talent'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Users className="w-4 h-4 inline mr-2" />
            Talent Matrix
          </button>
          <button
            onClick={() => setActiveTab('demographic')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === 'demographic'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Target className="w-4 h-4 inline mr-2" />
            Demographics
          </button>
        </div>
      </div>

      {/* Grade Performance */}
      {activeTab === 'grade' && (
        <div className="space-y-6">
          <div className="card bg-gray-900">
            <h2 className="text-xl font-bold text-white mb-4">
              Director Grade vs IMDB Rating Performance
            </h2>
            <div style={{ height: '400px' }}>
              <Bar data={gradePerformanceData} options={chartOptions} />
            </div>
          </div>

          {analytics.grade_performance.outliers.length > 0 && (
            <div className="card">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">
                Top Performers (Exceeded Expectations)
              </h3>
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Movie</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Director</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Grade</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Rating</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Expected</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Difference</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {analytics.grade_performance.outliers.slice(0, 5).map((outlier, index) => (
                      <tr key={index}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                          {outlier.movie_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {outlier.director}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {outlier.grade}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-semibold">
                          {outlier.rating.toFixed(2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {outlier.expected.toFixed(2)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 font-semibold">
                          +{outlier.difference.toFixed(2)}
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

      {/* Genre Timeline */}
      {activeTab === 'timeline' && (
        <div className="card bg-gray-900">
          <h2 className="text-xl font-bold text-white mb-4">
            Genre Popularity Over Time (Quarterly)
          </h2>
          <div style={{ height: '400px' }}>
            <Line data={genreTimelineData} options={chartOptions} />
          </div>
        </div>
      )}

      {/* Talent Matrix */}
      {activeTab === 'talent' && (
        <div className="card bg-gray-900">
          <h2 className="text-xl font-bold text-white mb-4">
            Hero Performance Matrix (Bubble size = Movie count)
          </h2>
          <div style={{ height: '500px' }}>
            <Bubble data={talentMatrixData} options={talentMatrixOptions} />
          </div>
        </div>
      )}

      {/* Demographics Heatmap */}
      {activeTab === 'demographic' && (
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Genre-Age Group Popularity Matrix
          </h2>
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr>
                  <th className="px-4 py-2 bg-gray-100 text-left text-sm font-semibold text-gray-700">
                    Genre / Age Group
                  </th>
                  {analytics.demographic_heatmap.age_groups.map(age => (
                    <th key={age} className="px-4 py-2 bg-gray-100 text-center text-sm font-semibold text-gray-700">
                      {age}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {analytics.demographic_heatmap.genres.map(genre => (
                  <tr key={genre} className="border-t">
                    <td className="px-4 py-2 font-medium text-gray-900">{genre}</td>
                    {analytics.demographic_heatmap.age_groups.map(age => {
                      const cell = analytics.demographic_heatmap.data.find(
                        d => d.genre === genre && d.age_group === age
                      )
                      const value = cell ? cell.popularity : 0
                      const intensity = Math.min(value / 50, 1)
                      const bgColor = `rgba(59, 130, 246, ${intensity * 0.7})`
                      
                      return (
                        <td
                          key={age}
                          className="px-4 py-2 text-center text-sm"
                          style={{ backgroundColor: bgColor }}
                        >
                          <span className={intensity > 0.5 ? 'text-white font-semibold' : 'text-gray-700'}>
                            {value.toFixed(1)}
                          </span>
                        </td>
                      )
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
