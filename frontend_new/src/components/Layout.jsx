import { Outlet, Link, useNavigate } from 'react-router-dom'
import { Film, LogOut, Home, Plus, BarChart3 } from 'lucide-react'
import { useAuthStore } from '../store/authStore'

export default function Layout() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link to="/" className="flex items-center space-x-2">
                <Film className="w-8 h-8 text-blue-600" />
                <span className="text-xl font-bold text-gray-900">Film Intel</span>
              </Link>
              
              <div className="hidden md:flex space-x-4">
                <Link to="/" className="flex items-center space-x-1 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100">
                  <Home className="w-4 h-4" />
                  <span>Dashboard</span>
                </Link>
                <Link to="/movies" className="flex items-center space-x-1 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100">
                  <Film className="w-4 h-4" />
                  <span>My Movies</span>
                </Link>
                <Link to="/analytics" className="flex items-center space-x-1 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100">
                  <BarChart3 className="w-4 h-4" />
                  <span>Analytics</span>
                </Link>
                <Link to="/movies/create" className="flex items-center space-x-1 px-3 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700">
                  <Plus className="w-4 h-4" />
                  <span>New Project</span>
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-700">
                <span className="font-medium">{user?.username || 'Producer'}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-1 px-3 py-2 rounded-md text-gray-700 hover:bg-gray-100"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Outlet />
      </main>
    </div>
  )
}
