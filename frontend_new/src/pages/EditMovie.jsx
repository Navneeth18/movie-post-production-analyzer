import { useState, useEffect } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import toast from 'react-hot-toast'
import { movieAPI } from '../services/api'

const GENRE_OPTIONS = ['Action', 'Drama', 'Comedy', 'Thriller', 'Romance', 'Horror', 'Sci-Fi', 'Fantasy', 'Crime', 'Mystery']
const LANGUAGE_OPTIONS = ['Telugu', 'Hindi', 'Tamil', 'Malayalam', 'Kannada', 'English', 'Bengali', 'Marathi']

export default function EditMovie() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    director: '',
    genres: [],
    budget: '',
    languages: [],
    region: '',
    release_date: '',
    status: 'pre-production',
    cast: []
  })

  const [castMember, setCastMember] = useState({ name: '', role: '', star_power: '' })

  useEffect(() => {
    loadMovie()
  }, [id])

  const loadMovie = async () => {
    try {
      const { data } = await movieAPI.getMovie(id)
      setFormData({
        title: data.title,
        director: data.director,
        genres: data.genres || [],
        budget: (data.budget / 10000000).toString(),
        languages: data.languages || [],
        region: data.region,
        release_date: data.release_date ? data.release_date.split('T')[0] : '',
        status: data.status,
        cast: data.cast || []
      })
    } catch (error) {
      toast.error('Failed to load movie')
      navigate('/movies')
    } finally {
      setLoading(false)
    }
  }

  const toggleGenre = (genre) => {
    setFormData(prev => ({
      ...prev,
      genres: prev.genres.includes(genre)
        ? prev.genres.filter(g => g !== genre)
        : [...prev.genres, genre]
    }))
  }

  const toggleLanguage = (language) => {
    setFormData(prev => ({
      ...prev,
      languages: prev.languages.includes(language)
        ? prev.languages.filter(l => l !== language)
        : [...prev.languages, language]
    }))
  }

  const addCastMember = () => {
    if (!castMember.name || !castMember.role) {
      toast.error('Please fill cast member details')
      return
    }

    setFormData({
      ...formData,
      cast: [...formData.cast, {
        name: castMember.name,
        role: castMember.role,
        star_power: parseFloat(castMember.star_power) || 50
      }]
    })
    setCastMember({ name: '', role: '', star_power: '' })
  }

  const removeCastMember = (index) => {
    setFormData({
      ...formData,
      cast: formData.cast.filter((_, i) => i !== index)
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (formData.genres.length === 0) {
      toast.error('Please select at least one genre')
      return
    }

    if (formData.languages.length === 0) {
      toast.error('Please select at least one language')
      return
    }

    setSaving(true)

    try {
      const payload = {
        ...formData,
        budget: parseFloat(formData.budget) * 10000000,
        release_date: formData.release_date ? new Date(formData.release_date).toISOString() : null
      }

      await movieAPI.updateMovie(id, payload)
      toast.success('Movie updated successfully!')
      navigate(`/movies/${id}`)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to update movie')
    } finally {
      setSaving(false)
    }
  }

  if (loading) {
    return <div className="text-center py-12">Loading...</div>
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <button
        onClick={() => navigate(`/movies/${id}`)}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movie</span>
      </button>

      <div className="card">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Edit Movie Project</h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">Movie Title *</label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                className="input"
                required
              />
            </div>

            <div>
              <label className="label">Director *</label>
              <input
                type="text"
                value={formData.director}
                onChange={(e) => setFormData({...formData, director: e.target.value})}
                className="input"
                required
              />
            </div>
          </div>

          <div>
            <label className="label">Genres * (Select multiple)</label>
            <div className="flex flex-wrap gap-2">
              {GENRE_OPTIONS.map(genre => (
                <button
                  key={genre}
                  type="button"
                  onClick={() => toggleGenre(genre)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    formData.genres.includes(genre)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {genre}
                </button>
              ))}
            </div>
            {formData.genres.length > 0 && (
              <p className="text-sm text-gray-600 mt-2">
                Selected: {formData.genres.join(', ')}
              </p>
            )}
          </div>

          <div>
            <label className="label">Languages * (Select multiple)</label>
            <div className="flex flex-wrap gap-2">
              {LANGUAGE_OPTIONS.map(language => (
                <button
                  key={language}
                  type="button"
                  onClick={() => toggleLanguage(language)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    formData.languages.includes(language)
                      ? 'bg-green-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {language}
                </button>
              ))}
            </div>
            {formData.languages.length > 0 && (
              <p className="text-sm text-gray-600 mt-2">
                Selected: {formData.languages.join(', ')}
              </p>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">Budget (in Crores) *</label>
              <input
                type="number"
                step="0.1"
                value={formData.budget}
                onChange={(e) => setFormData({...formData, budget: e.target.value})}
                className="input"
                required
              />
            </div>

            <div>
              <label className="label">Region *</label>
              <input
                type="text"
                value={formData.region}
                onChange={(e) => setFormData({...formData, region: e.target.value})}
                className="input"
                required
              />
            </div>

            <div>
              <label className="label">Release Date</label>
              <input
                type="date"
                value={formData.release_date}
                onChange={(e) => setFormData({...formData, release_date: e.target.value})}
                className="input"
              />
            </div>

            <div>
              <label className="label">Status *</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({...formData, status: e.target.value})}
                className="input"
                required
              >
                <option value="pre-production">Pre-Production</option>
                <option value="production">Production</option>
                <option value="post-production">Post-Production</option>
                <option value="awaiting-release">Awaiting Release</option>
                <option value="released">Released</option>
              </select>
            </div>
          </div>

          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold mb-4">Cast Members</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
              <input
                type="text"
                placeholder="Actor Name"
                value={castMember.name}
                onChange={(e) => setCastMember({...castMember, name: e.target.value})}
                className="input"
              />
              <input
                type="text"
                placeholder="Role"
                value={castMember.role}
                onChange={(e) => setCastMember({...castMember, role: e.target.value})}
                className="input"
              />
              <input
                type="number"
                placeholder="Star Power (0-100)"
                value={castMember.star_power}
                onChange={(e) => setCastMember({...castMember, star_power: e.target.value})}
                className="input"
              />
              <button
                type="button"
                onClick={addCastMember}
                className="btn btn-secondary"
              >
                Add Cast
              </button>
            </div>

            {formData.cast.length > 0 && (
              <div className="space-y-2">
                {formData.cast.map((member, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <span className="font-medium">{member.name}</span>
                      <span className="text-gray-600"> as {member.role}</span>
                      <span className="text-sm text-gray-500"> (Star Power: {member.star_power})</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => removeCastMember(index)}
                      className="text-red-600 hover:text-red-800"
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex space-x-4">
            <button
              type="submit"
              disabled={saving}
              className="btn btn-primary flex-1"
            >
              {saving ? 'Saving...' : 'Save Changes'}
            </button>
            <button
              type="button"
              onClick={() => navigate(`/movies/${id}`)}
              className="btn btn-secondary"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
