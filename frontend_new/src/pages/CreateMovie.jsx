import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowLeft } from 'lucide-react'
import toast from 'react-hot-toast'
import { movieAPI } from '../services/api'

export default function CreateMovie() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({
    title: '',
    director: '',
    genre: 'Drama',
    budget: '',
    language: 'Hindi',
    themes: '',
    region: 'Pan-India',
    release_date: '',
    status: 'pre-production',
    cast: []
  })

  const [castMember, setCastMember] = useState({ name: '', role: '', star_power: '' })

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
    setLoading(true)

    try {
      const payload = {
        ...formData,
        budget: parseFloat(formData.budget) * 10000000, // Convert Cr to actual value
        release_date: formData.release_date ? new Date(formData.release_date).toISOString() : null
      }

      const { data } = await movieAPI.createMovie(payload)
      toast.success('Movie created successfully!')
      navigate(`/movies/${data.id}`)
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to create movie')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <button
        onClick={() => navigate('/movies')}
        className="flex items-center space-x-2 text-gray-600 hover:text-gray-900"
      >
        <ArrowLeft className="w-5 h-5" />
        <span>Back to Movies</span>
      </button>

      <div className="card">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Create New Movie Project</h1>

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

            <div>
              <label className="label">Genre *</label>
              <select
                value={formData.genre}
                onChange={(e) => setFormData({...formData, genre: e.target.value})}
                className="input"
                required
              >
                <option>Drama</option>
                <option>Thriller</option>
                <option>Action</option>
                <option>Comedy</option>
                <option>Romance</option>
                <option>Horror</option>
              </select>
            </div>

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
              <label className="label">Language *</label>
              <select
                value={formData.language}
                onChange={(e) => setFormData({...formData, language: e.target.value})}
                className="input"
                required
              >
                <option>Hindi</option>
                <option>Telugu</option>
                <option>Tamil</option>
                <option>Malayalam</option>
                <option>Kannada</option>
                <option>Bengali</option>
              </select>
            </div>

            <div>
              <label className="label">Region *</label>
              <input
                type="text"
                value={formData.region}
                onChange={(e) => setFormData({...formData, region: e.target.value})}
                className="input"
                placeholder="e.g., Pan-India, South India"
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
              </select>
            </div>
          </div>

          <div>
            <label className="label">Themes</label>
            <textarea
              value={formData.themes}
              onChange={(e) => setFormData({...formData, themes: e.target.value})}
              className="input"
              rows="3"
              placeholder="e.g., Family, Drama, Social Issues"
            />
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
              disabled={loading}
              className="btn btn-primary flex-1"
            >
              {loading ? 'Creating...' : 'Create Movie'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/movies')}
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
