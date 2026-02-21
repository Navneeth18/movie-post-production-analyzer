import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, TrendingUp, AlertCircle } from 'lucide-react'
import { movieAPI, budgetAPI } from '../services/api'
import toast from 'react-hot-toast'

// Simple markdown formatter for AI output
const formatMarkdown = (text) => {
  if (!text) return null

  // Split into lines
  const lines = text.split('\n')
  const elements = []
  let currentList = []
  let inCodeBlock = false
  let codeBlockContent = []

  const flushList = () => {
    if (currentList.length > 0) {
      elements.push(
        <ul key={`list-${elements.length}`} className="list-disc list-inside ml-4 mb-4 space-y-2">
          {currentList.map((item, i) => (
            <li key={i} className="text-gray-700 leading-relaxed">{item}</li>
          ))}
        </ul>
      )
      currentList = []
    }
  }

  const flushCodeBlock = () => {
    if (codeBlockContent.length > 0) {
      elements.push(
        <pre key={`code-${elements.length}`} className="bg-gray-100 p-4 rounded-lg mb-4 overflow-x-auto">
          <code className="text-sm text-gray-800 font-mono">
            {codeBlockContent.join('\n')}
          </code>
        </pre>
      )
      codeBlockContent = []
    }
  }

  const formatInlineStyles = (text) => {
    // Bold **text**
    let formatted = text.replace(/\*\*(.+?)\*\*/g, '<strong class="font-semibold text-gray-900">$1</strong>')
    // Italic *text*
    formatted = formatted.replace(/\*(.+?)\*/g, '<em class="italic">$1</em>')
    // Inline code `code`
    formatted = formatted.replace(/`(.+?)`/g, '<code class="bg-gray-100 px-2 py-1 rounded text-sm font-mono text-gray-800">$1</code>')
    // Currency symbols
    formatted = formatted.replace(/₹/g, '<span class="text-yellow-600 font-semibold">₹</span>')
    return formatted
  }

  lines.forEach((line, index) => {
    const trimmed = line.trim()

    // Code blocks ```
    if (trimmed.startsWith('```')) {
      if (inCodeBlock) {
        flushCodeBlock()
        inCodeBlock = false
      } else {
        flushList()
        inCodeBlock = true
      }
      return
    }

    if (inCodeBlock) {
      codeBlockContent.push(line)
      return
    }

    // Skip empty lines
    if (!trimmed) {
      flushList()
      elements.push(<div key={`space-${index}`} className="h-2" />)
      return
    }

    // Headers (# ## ### ####)
    if (trimmed.startsWith('####')) {
      flushList()
      elements.push(
        <h4 key={`h4-${index}`} className="text-base font-semibold text-gray-800 mt-4 mb-2">
          {trimmed.replace(/^####\s*/, '')}
        </h4>
      )
    } else if (trimmed.startsWith('###')) {
      flushList()
      elements.push(
        <h3 key={`h3-${index}`} className="text-lg font-semibold text-gray-800 mt-5 mb-2">
          {trimmed.replace(/^###\s*/, '')}
        </h3>
      )
    } else if (trimmed.startsWith('##')) {
      flushList()
      elements.push(
        <h2 key={`h2-${index}`} className="text-xl font-bold text-gray-900 mt-6 mb-3 pb-2 border-b border-gray-200">
          {trimmed.replace(/^##\s*/, '')}
        </h2>
      )
    } else if (trimmed.startsWith('#')) {
      flushList()
      elements.push(
        <h1 key={`h1-${index}`} className="text-2xl font-bold text-gray-900 mt-6 mb-4 pb-2 border-b-2 border-yellow-500">
          {trimmed.replace(/^#\s*/, '')}
        </h1>
      )
    }
    // Bullet points (- or *)
    else if (trimmed.match(/^[-*]\s+/)) {
      const content = trimmed.replace(/^[-*]\s+/, '')
      const formatted = formatInlineStyles(content)
      currentList.push(<span dangerouslySetInnerHTML={{ __html: formatted }} />)
    }
    // Numbered lists
    else if (/^\d+\.\s/.test(trimmed)) {
      flushList()
      const content = trimmed.replace(/^\d+\.\s*/, '')
      const formatted = formatInlineStyles(content)
      const number = trimmed.match(/^\d+/)[0]
      elements.push(
        <div key={`num-${index}`} className="flex mb-2 ml-4">
          <span className="font-semibold text-yellow-600 mr-2 flex-shrink-0">{number}.</span>
          <span className="text-gray-700" dangerouslySetInnerHTML={{ __html: formatted }} />
        </div>
      )
    }
    // Blockquote
    else if (trimmed.startsWith('>')) {
      flushList()
      const content = trimmed.replace(/^>\s*/, '')
      const formatted = formatInlineStyles(content)
      elements.push(
        <blockquote key={`quote-${index}`} className="border-l-4 border-yellow-500 pl-4 py-2 mb-3 italic text-gray-600">
          <span dangerouslySetInnerHTML={{ __html: formatted }} />
        </blockquote>
      )
    }
    // Regular paragraph
    else {
      flushList()
      const formatted = formatInlineStyles(trimmed)
      elements.push(
        <p key={`p-${index}`} className="text-gray-700 mb-3 leading-relaxed" dangerouslySetInnerHTML={{ __html: formatted }} />
      )
    }
  })

  flushList()
  flushCodeBlock()
  
  return <div className="markdown-content">{elements}</div>
}

export default function BudgetPlanning() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [aiResult, setAiResult] = useState('')
  
  const [totalBudget, setTotalBudget] = useState(5000000) // ₹50L default
  const [allocations, setAllocations] = useState({
    digital: 30,
    traditional: 15,
    influencer: 20,
    events: 10,
    pr: 15,
    contingency: 10
  })
  const [timeline, setTimeline] = useState(8) // weeks
  const [selectedChannel, setSelectedChannel] = useState(null)

  const channels = {
    digital: {
      name: "Digital Marketing",
      icon: "◎",
      subChannels: ["Social Media Ads", "YouTube Pre-roll", "Display Ads", "Search Ads"],
      avgROI: 3.2,
      minBudget: 500000,
      optimalRange: "25-35%"
    },
    traditional: {
      name: "Traditional Media",
      icon: "⬢",
      subChannels: ["TV Spots", "Print Ads", "Radio", "Outdoor"],
      avgROI: 1.8,
      minBudget: 1000000,
      optimalRange: "10-20%"
    },
    influencer: {
      name: "Influencer Marketing",
      icon: "⬡",
      subChannels: ["Micro Influencers", "Macro Influencers", "Celebrity", "Content Creators"],
      avgROI: 2.5,
      minBudget: 300000,
      optimalRange: "15-25%"
    },
    events: {
      name: "Events & Activations",
      icon: "◆",
      subChannels: ["Premiere", "Fan Meetups", "College Tours", "Mall Activations"],
      avgROI: 2.0,
      minBudget: 500000,
      optimalRange: "8-15%"
    },
    pr: {
      name: "PR & Media Relations",
      icon: "◈",
      subChannels: ["Press Releases", "Interviews", "Media Kit", "Junkets"],
      avgROI: 2.8,
      minBudget: 200000,
      optimalRange: "10-20%"
    },
    contingency: {
      name: "Contingency Reserve",
      icon: "⊕",
      subChannels: ["Emergency Response", "Opportunity Buys", "Crisis Management"],
      avgROI: 0,
      minBudget: 0,
      optimalRange: "10-15%"
    }
  }

  useEffect(() => {
    loadMovie()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await movieAPI.getMovie(id)
      
      if (data.tag === 'past') {
        toast.error('Budget planning is only available for current movies')
        navigate(`/movies/${id}`)
        return
      }
      
      setMovie(data)
      
      // Load existing budget plan
      try {
        const { data: budgetData } = await budgetAPI.getBudgetPlan(id)
        if (budgetData) {
          setTotalBudget(budgetData.total_budget)
          setAllocations(budgetData.allocations)
          setTimeline(budgetData.timeline_weeks)
        }
      } catch (error) {
        // No existing budget plan, use defaults
        console.log('No existing budget plan')
      }
      
    } catch (error) {
      toast.error('Failed to load movie')
      navigate('/movies')
    } finally {
      setLoading(false)
    }
  }

  const calculateAmount = (percentage) => {
    return (totalBudget * percentage) / 100
  }

  const formatCurrency = (amount) => {
    if (amount >= 10000000) return `₹${(amount / 10000000).toFixed(2)}Cr`
    if (amount >= 100000) return `₹${(amount / 100000).toFixed(2)}L`
    return `₹${(amount / 1000).toFixed(0)}K`
  }

  const totalAllocated = Object.values(allocations).reduce((sum, val) => sum + val, 0)
  const remainingBudget = totalBudget - (totalBudget * totalAllocated / 100)

  const calculateProjectedROI = () => {
    return Object.entries(allocations).reduce((total, [key, percentage]) => {
      const amount = calculateAmount(percentage)
      const roi = channels[key].avgROI
      return total + (amount * roi)
    }, 0)
  }

  const getHealthStatus = () => {
    if (totalAllocated > 100) return { color: "#f87171", text: "Over Budget", icon: "⚠" }
    if (totalAllocated < 85) return { color: "#fbbf24", text: "Under-allocated", icon: "⚡" }
    return { color: "#4ade80", text: "Optimal", icon: "✓" }
  }

  const saveBudgetPlan = async () => {
    if (totalAllocated > 100) {
      toast.error('Total allocation cannot exceed 100%')
      return
    }

    try {
      setSaving(true)
      
      await budgetAPI.createOrUpdateBudgetPlan(id, {
        total_budget: totalBudget,
        allocations: allocations,
        timeline_weeks: timeline
      })
      
      toast.success('Budget plan saved successfully!')
    } catch (error) {
      toast.error('Failed to save budget plan')
    } finally {
      setSaving(false)
    }
  }

  const runAI = async () => {
    setAiLoading(true)
    setAiResult('')

    try {
      const { data } = await budgetAPI.optimizeBudget(id, {
        movie_title: movie.title,
        genre: movie.genres[0] || 'Drama',
        budget: movie.budget || 50000000,
        total_marketing_budget: totalBudget,
        timeline_weeks: timeline,
        current_allocations: allocations
      })

      setAiResult(data.recommendations)
      
      // Show source indicator
      if (data.source === 'deepseek-r1') {
        toast.success('Optimization generated by DeepSeek R1', { duration: 3000 })
      } else if (data.source === 'fallback') {
        toast('Using rule-based recommendations (AI unavailable)', { 
          icon: '⚠️',
          duration: 3000 
        })
      }
    } catch (error) {
      toast.error('Failed to generate optimization')
    } finally {
      setAiLoading(false)
    }
  }

  const applyOptimalAllocation = () => {
    const genre = movie.genres[0]?.toLowerCase() || 'drama'
    
    let optimal
    if (genre === 'drama' || genre === 'romance') {
      optimal = { digital: 28, traditional: 12, influencer: 22, events: 12, pr: 18, contingency: 8 }
    } else if (genre === 'action' || genre === 'thriller' || genre === 'sci-fi') {
      optimal = { digital: 38, traditional: 10, influencer: 22, events: 10, pr: 12, contingency: 8 }
    } else if (genre === 'comedy' || genre === 'family') {
      optimal = { digital: 35, traditional: 12, influencer: 25, events: 15, pr: 8, contingency: 5 }
    } else {
      optimal = { digital: 35, traditional: 15, influencer: 20, events: 10, pr: 12, contingency: 8 }
    }
    
    setAllocations(optimal)
    toast.success(`Applied optimal allocation for ${genre} genre`)
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!movie) {
    return <div className="text-center py-12">Movie not found</div>
  }

  const health = getHealthStatus()
  const projectedROI = calculateProjectedROI()
  const projectedRevenue = projectedROI

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <button
        onClick={() => navigate(`/movies/${id}`)}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movie</span>
      </button>

      <div className="card">
        <div className="flex justify-between items-start mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              Promotion <span className="text-yellow-600">Budget</span> Planning
            </h1>
            <p className="text-gray-600">Strategic allocation & ROI optimization — {movie.title}</p>
          </div>
          <button
            onClick={saveBudgetPlan}
            disabled={saving || totalAllocated > 100}
            className="btn btn-primary"
          >
            {saving ? 'Saving...' : 'Save Budget Plan'}
          </button>
        </div>

        {/* Budget Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="card bg-gray-50">
            <div className="text-sm text-gray-600 mb-2">Total Budget</div>
            <div className="text-2xl font-bold text-gray-900 mb-3">{formatCurrency(totalBudget)}</div>
            <input
              type="range"
              min="1000000"
              max="50000000"
              step="500000"
              value={totalBudget}
              onChange={e => setTotalBudget(parseInt(e.target.value))}
              className="w-full accent-yellow-600"
            />
          </div>

          <div className="card bg-gray-50">
            <div className="text-sm text-gray-600 mb-2">Allocated</div>
            <div className="text-2xl font-bold mb-1" style={{ color: health.color }}>
              {totalAllocated}%
            </div>
            <div className="text-xs" style={{ color: health.color }}>
              {health.icon} {health.text}
            </div>
          </div>

          <div className="card bg-gray-50">
            <div className="text-sm text-gray-600 mb-2">Projected ROI</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">
              {(projectedROI / totalBudget).toFixed(1)}x
            </div>
            <div className="text-xs text-gray-600">{formatCurrency(projectedRevenue)} return</div>
          </div>

          <div className="card bg-gray-50">
            <div className="text-sm text-gray-600 mb-2">Timeline</div>
            <div className="text-2xl font-bold text-gray-900 mb-1">{timeline}</div>
            <div className="text-xs text-gray-600 mb-2">weeks pre-release</div>
            <input
              type="range"
              min="4"
              max="16"
              value={timeline}
              onChange={e => setTimeline(parseInt(e.target.value))}
              className="w-full accent-yellow-600"
            />
          </div>
        </div>

        {/* Channel Allocation */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <div className="card bg-gray-50">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                Channel <span className="text-yellow-600">Allocation</span>
              </h3>
              <button
                className="btn btn-outline text-sm"
                onClick={applyOptimalAllocation}
              >
                Apply Optimal
              </button>
            </div>

            {Object.entries(channels).map(([key, channel]) => {
              const amount = calculateAmount(allocations[key])
              const isUnderMin = amount < channel.minBudget && allocations[key] > 0

              return (
                <div key={key} className="mb-5">
                  <div className="flex justify-between items-center mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="text-xl text-yellow-600">{channel.icon}</span>
                      <label
                        className="text-sm text-gray-700 cursor-pointer hover:text-gray-900"
                        onClick={() => setSelectedChannel(key)}
                      >
                        {channel.name}
                      </label>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className="text-xs text-gray-500">{channel.optimalRange}</span>
                      <span className={`text-sm font-medium ${isUnderMin ? 'text-red-500' : 'text-yellow-600'}`}>
                        {allocations[key]}% · {formatCurrency(amount)}
                      </span>
                    </div>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="50"
                    value={allocations[key]}
                    onChange={e => setAllocations(prev => ({ ...prev, [key]: parseInt(e.target.value) }))}
                    className={`w-full ${isUnderMin ? 'accent-red-500' : 'accent-yellow-600'}`}
                  />
                  {isUnderMin && (
                    <div className="text-xs text-red-500 mt-1">
                      <AlertCircle className="w-3 h-3 inline mr-1" />
                      Below minimum recommended: {formatCurrency(channel.minBudget)}
                    </div>
                  )}
                </div>
              )
            })}

            <div className="pt-4 border-t border-gray-200 mt-4">
              <div className="flex justify-between items-center">
                <span className="text-xs text-gray-600 uppercase tracking-wider">Total Allocated</span>
                <span className="text-lg font-bold" style={{ color: health.color }}>
                  {totalAllocated}% · {formatCurrency(totalBudget * totalAllocated / 100)}
                </span>
              </div>
              {remainingBudget !== 0 && (
                <div className={`text-xs mt-2 text-right ${remainingBudget > 0 ? 'text-green-500' : 'text-red-500'}`}>
                  {remainingBudget > 0 ? 'Remaining' : 'Over'}: {formatCurrency(Math.abs(remainingBudget))}
                </div>
              )}
            </div>
          </div>

          {/* Channel Details */}
          <div className="card bg-gray-50">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Channel <span className="text-yellow-600">Details</span>
            </h3>
            {selectedChannel ? (
              <>
                <div className="flex items-center space-x-3 mb-4">
                  <span className="text-4xl text-yellow-600">{channels[selectedChannel].icon}</span>
                  <div>
                    <div className="text-xl font-semibold text-gray-900">{channels[selectedChannel].name}</div>
                    <div className="text-xs text-gray-600">
                      Avg ROI: {channels[selectedChannel].avgROI}x · Min: {formatCurrency(channels[selectedChannel].minBudget)}
                    </div>
                  </div>
                </div>

                <div className="mb-4">
                  <div className="text-xs text-gray-600 uppercase tracking-wider mb-2">Current Allocation</div>
                  <div className="text-3xl font-bold text-yellow-600 mb-1">
                    {formatCurrency(calculateAmount(allocations[selectedChannel]))}
                  </div>
                  <div className="text-sm text-gray-600">{allocations[selectedChannel]}% of total budget</div>
                </div>

                <div className="mb-4">
                  <div className="text-xs text-gray-600 uppercase tracking-wider mb-2">Sub-Channels</div>
                  <div className="flex flex-wrap gap-2">
                    {channels[selectedChannel].subChannels.map(sub => (
                      <span key={sub} className="px-2 py-1 bg-gray-200 text-gray-700 text-xs rounded">
                        {sub}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <div className="text-xs text-gray-600 uppercase tracking-wider mb-2">Projected Return</div>
                  <div className="text-2xl font-bold text-green-500">
                    {formatCurrency(calculateAmount(allocations[selectedChannel]) * channels[selectedChannel].avgROI)}
                  </div>
                </div>
              </>
            ) : (
              <div className="py-12 text-center text-gray-500 text-sm">
                Click on a channel to see details
              </div>
            )}
          </div>
        </div>

        {/* Timeline Breakdown */}
        <div className="card bg-gray-50 mb-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Spending <span className="text-yellow-600">Timeline</span> — {timeline} Week Strategy
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {[
              { phase: `Weeks ${timeline}-6`, focus: "Awareness", spend: 25, activities: "Teaser, Social buzz, PR seeding" },
              { phase: "Weeks 5-3", focus: "Interest", spend: 35, activities: "Trailer launch, Influencer campaigns" },
              { phase: "Weeks 2-1", focus: "Desire", spend: 30, activities: "Heavy digital, Events, Final push" },
              { phase: "Week 0", focus: "Action", spend: 10, activities: "Release day, Real-time engagement" },
            ].map((item, i) => (
              <div key={i} className="card bg-white">
                <div className="text-xs text-yellow-600 uppercase tracking-wider mb-2">{item.phase}</div>
                <div className="text-xl font-bold text-gray-900 mb-1">{item.focus}</div>
                <div className="text-3xl font-bold text-yellow-600 mb-2">{item.spend}%</div>
                <div className="text-xs text-gray-600 leading-relaxed mb-2">{item.activities}</div>
                <div className="text-sm text-gray-700 font-medium">
                  {formatCurrency((totalBudget * totalAllocated / 100) * item.spend / 100)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Optimization */}
        <div className="card bg-gray-50">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            AI <span className="text-yellow-600">Budget</span> Optimization
          </h3>
          <button
            className="btn btn-primary mb-4 flex items-center space-x-2"
            onClick={runAI}
            disabled={aiLoading}
          >
            <TrendingUp className="w-4 h-4" />
            <span>{aiLoading ? 'Analyzing with DeepSeek R1 (may take 2-3 minutes)...' : 'Generate AI Optimization Strategy'}</span>
          </button>
          {(aiLoading || aiResult) && (
            <div className="bg-white border border-gray-200 rounded-lg p-4">
              {aiLoading ? (
                <div className="text-gray-600">
                  <div className="flex items-center space-x-2 mb-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-yellow-600"></div>
                    <span>DeepSeek R1 is analyzing your budget allocation...</span>
                  </div>
                  <p className="text-xs text-gray-500">This may take 2-3 minutes as the AI performs deep reasoning</p>
                </div>
              ) : (
                <div className="ai-recommendations">
                  {formatMarkdown(aiResult)}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
