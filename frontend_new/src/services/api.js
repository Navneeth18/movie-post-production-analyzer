import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth endpoints
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getMe: () => api.get('/auth/me'),
}

// Movie endpoints
export const movieAPI = {
  getMyMovies: () => api.get('/movies/'),
  getAllMovies: (tag = 'current') => api.get(`/movies/all?tag=${tag}`),
  getMovie: (id) => api.get(`/movies/${id}`),
  createMovie: (data) => api.post('/movies/', data),
  updateMovie: (id, data) => api.put(`/movies/${id}`, data),
  deleteMovie: (id) => api.delete(`/movies/${id}`),
  analyzeCompetitor: (movieId, competitorId) => 
    api.post(`/movies/${movieId}/analyze-competitor`, { competitor_movie_id: competitorId }),
  getCompetitors: (movieId) => api.get(`/movies/${movieId}/competitors`),
}

// Public Pulse endpoints
export const publicPulseAPI = {
  addTrailer: (movieId, youtubeUrl) => 
    api.post(`/public-pulse/${movieId}/add-trailer`, { youtube_url: youtubeUrl }),
  refreshPulse: (movieId) => 
    api.post(`/public-pulse/${movieId}/refresh-pulse`),
  getCurrentPulse: (movieId) => 
    api.get(`/public-pulse/${movieId}/current`),
  getPulseHistory: (movieId) => 
    api.get(`/public-pulse/${movieId}/history`),
  removeTrailer: (movieId) => 
    api.delete(`/public-pulse/${movieId}/trailer`),
}

// Release strategy endpoints
export const releaseStrategyAPI = {
  analyzeDateRange: (data) => api.post('/release-strategy/analyze-date-range', data),
  generatePRStrategy: (data) => api.post('/release-strategy/pr-strategy', data),
  getReleaseDateDecision: (data) => api.post('/release-strategy/release-date-decision', data),
}

// Facebook Campaign endpoints
export const facebookCampaignAPI = {
  generateContent: (movieId, campaignType) =>
    api.post(`/facebook-campaign/${movieId}/generate-content`, { campaign_type: campaignType }),
  createPost: (movieId, postData) =>
    api.post(`/facebook-campaign/${movieId}/create-post`, postData),
  getCampaignSchedule: (movieId, durationDays = 30) =>
    api.get(`/facebook-campaign/${movieId}/campaign-schedule?campaign_duration_days=${durationDays}`),
  getMoviePosts: (movieId) =>
    api.get(`/facebook-campaign/${movieId}/posts`),
  getPostInsights: (postId) =>
    api.get(`/facebook-campaign/post/${postId}/insights`),
  deletePost: (postId) =>
    api.delete(`/facebook-campaign/post/${postId}`),
}

export default api
