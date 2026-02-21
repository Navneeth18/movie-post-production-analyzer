import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, Send } from 'lucide-react'
import { movieAPI, facebookCampaignAPI } from '../services/api'
import toast from 'react-hot-toast'

export default function FacebookCampaign() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [posting, setPosting] = useState(false)
  
  // Form fields matching your script's requirements
  const [movieName, setMovieName] = useState('')
  const [heroName, setHeroName] = useState('')
  const [heroineName, setHeroineName] = useState('')
  const [directorName, setDirectorName] = useState('')
  const [genre, setGenre] = useState('action')
  const [releaseDate, setReleaseDate] = useState('')
  const [requirementsPoster, setRequirementsPoster] = useState('')

  useEffect(() => {
    loadMovie()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await movieAPI.getMovie(id)
      if (data.tag === 'past') {
        toast.error('Facebook campaigns are only available for unreleased movies')
        navigate(`/movies/${id}`)
        return
      }
      setMovie(data)
      
      // Pre-fill form with movie data
      setMovieName(data.title || '')
      setDirectorName(data.director || '')
      setGenre(data.genres?.[0]?.toLowerCase() || 'action')
      setReleaseDate(data.release_date ? data.release_date.split('T')[0] : '')
      
      // Extract hero and heroine from cast
      const hero = data.cast?.find(c => c.role.includes('Hero') || c.role.includes('Lead 1'))
      const heroine = data.cast?.find(c => c.role.includes('Heroine') || c.role.includes('Lead 2'))
      
      if (hero) setHeroName(hero.name)
      if (heroine) setHeroineName(heroine.name)
      
    } catch (error) {
      toast.error('Failed to load movie')
      navigate('/movies')
    } finally {
      setLoading(false)
    }
  }

  const handleCreatePost = async () => {
    // Validate required fields
    if (!movieName || !heroName || !heroineName || !directorName || !genre) {
      toast.error('Please fill in all required fields')
      return
    }

    try {
      setPosting(true)
      
      const postData = {
        movie_name: movieName,
        hero_name: heroName,
        heroine_name: heroineName,
        director_name: directorName,
        genre: genre,
        release_date: releaseDate || null,
        requirements_poster: requirementsPoster || null
      }
      
      const { data } = await facebookCampaignAPI.createPost(id, postData)
      
      if (data.success === false) {
        const errorMsg = data.error || 'Failed to create post'
        
        if (errorMsg.includes('Failed to generate poster')) {
          toast.error('⚠️ AI poster generation failed. Please try again or contact support.', { duration: 5000 })
        } else if (data.error_code === 190) {
          toast.error('Facebook token expired! Please contact admin to refresh the token.')
        } else if (data.error_code === 200) {
          toast.error('Missing Facebook permissions. Please regenerate your token.')
        } else {
          toast.error(errorMsg)
        }
        return
      }
      
      if (data.mock) {
        toast.success('Post created in mock mode (Facebook API not configured)', { duration: 4000 })
      } else {
        toast.success('🎉 Post created on Facebook with AI-generated poster!')
      }
      
      // Reset optional fields
      setRequirementsPoster('')
      
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.response?.data?.error || 'Failed to create post'
      toast.error(errorMsg)
    } finally {
      setPosting(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  if (!movie) {
    return <div className="text-center py-12">Movie not found</div>
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <button
        onClick={() => navigate(`/movies/${id}`)}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movie</span>
      </button>

      <div className="card">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Facebook Campaign</h1>
        <p className="text-gray-600 mb-6">Create an AI-powered promotional post for {movie.title}</p>

        <div className="space-y-6">
          {/* Movie Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Movie Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={movieName}
              onChange={(e) => setMovieName(e.target.value)}
              className="input"
              placeholder="e.g., Leo 2"
              required
            />
          </div>

          {/* Hero Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Hero Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={heroName}
              onChange={(e) => setHeroName(e.target.value)}
              className="input"
              placeholder="e.g., Vijay"
              required
            />
          </div>

          {/* Heroine Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Heroine Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={heroineName}
              onChange={(e) => setHeroineName(e.target.value)}
              className="input"
              placeholder="e.g., Trisha"
              required
            />
          </div>

          {/* Director Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Director Name <span className="text-red-500">*</span>
            </label>
            <input
              type="text"
              value={directorName}
              onChange={(e) => setDirectorName(e.target.value)}
              className="input"
              placeholder="e.g., Lokesh Kanagaraj"
              required
            />
          </div>

          {/* Genre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Genre <span className="text-red-500">*</span>
            </label>
            <select
              value={genre}
              onChange={(e) => setGenre(e.target.value)}
              className="input"
              required
            >
              <option value="action">Action</option>
              <option value="romance">Romance</option>
              <option value="thriller">Thriller</option>
              <option value="horror">Horror</option>
              <option value="drama">Drama</option>
              <option value="fantasy">Fantasy</option>
              <option value="sci-fi">Sci-Fi</option>
              <option value="comedy">Comedy</option>
            </select>
          </div>

          {/* Release Date */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Release Date (optional)
            </label>
            <input
              type="date"
              value={releaseDate}
              onChange={(e) => setReleaseDate(e.target.value)}
              className="input"
            />
            <p className="text-xs text-gray-500 mt-1">
              Leave empty if release date is not confirmed
            </p>
          </div>

          {/* Poster Requirements */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Poster Requirements (optional)
            </label>
            <textarea
              value={requirementsPoster}
              onChange={(e) => setRequirementsPoster(e.target.value)}
              rows={4}
              className="input"
              placeholder="e.g., make the picture as hero is with a leopard walking in the snow and holding a hammer and make the text to be red"
            />
            <p className="text-xs text-gray-500 mt-1">
              Describe specific visual elements you want in the AI-generated poster
            </p>
          </div>

          {/* Info Box */}
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <h3 className="font-semibold text-blue-900 mb-2">What happens when you post:</h3>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>✓ AI generates a cinematic movie poster based on your inputs</li>
              <li>✓ Creates an engaging promotional caption with hashtags</li>
              <li>✓ Posts immediately to your Facebook page</li>
              <li>✓ Poster is customized for {genre} genre</li>
            </ul>
          </div>

          {/* Submit Button */}
          <button
            onClick={handleCreatePost}
            disabled={posting || !movieName || !heroName || !heroineName || !directorName || !genre}
            className="btn btn-primary w-full flex items-center justify-center space-x-2"
          >
            <Send className="w-5 h-5" />
            <span>
              {posting ? 'Creating Post & Generating Poster...' : 'Create Facebook Post Now'}
            </span>
          </button>
        </div>
      </div>
    </div>
  )
}
