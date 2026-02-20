import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Film } from 'lucide-react'
import toast from 'react-hot-toast'
import { authAPI } from '../services/api'

export default function Register() {
  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: ''
  })
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    // Validation
    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters')
      return
    }

    setLoading(true)

    try {
      const response = await authAPI.register(formData)
      console.log('Registration response:', response)
      toast.success('Registration successful! Please login.')
      navigate('/login')
    } catch (error) {
      console.error('Registration error:', error)
      const errorMessage = error.response?.data?.detail || 
                          error.message || 
                          'Registration failed. Please try again.'
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4">
      <div className="max-w-md w-full">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Film className="w-16 h-16 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">Film Intel Platform</h1>
          <p className="text-gray-600 mt-2">Create your producer account</p>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold mb-6">Register</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                className="input"
                placeholder="John Doe"
                required
              />
            </div>

            <div>
              <label className="label">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
                className="input"
                placeholder="johndoe"
                required
                minLength={3}
              />
              <p className="text-xs text-gray-500 mt-1">At least 3 characters</p>
            </div>

            <div>
              <label className="label">Email</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="input"
                placeholder="john@example.com"
                required
              />
            </div>

            <div>
              <label className="label">Password</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="input"
                placeholder="••••••••"
                required
                minLength={6}
              />
              <p className="text-xs text-gray-500 mt-1">At least 6 characters</p>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary w-full"
            >
              {loading ? 'Creating account...' : 'Register'}
            </button>
          </form>

          <p className="mt-4 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-600 hover:underline">
              Login here
            </Link>
          </p>
        </div>

        <div className="mt-4 text-center text-xs text-gray-500">
          <p>Make sure the backend is running at http://localhost:8000</p>
        </div>
      </div>
    </div>
  )
}
