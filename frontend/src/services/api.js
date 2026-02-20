import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Analytics endpoints
export const analyticsAPI = {
  getSentiment: (query) => api.get('/analytics/sentiment', { params: { query } }),
  getPulse: (query) => api.get('/analytics/pulse', { params: { query } }),
};

// Calculator endpoints
export const calculatorAPI = {
  calculateHWS: (data) => api.post('/calculator/hws', data),
};

// Marketing endpoints
export const marketingAPI = {
  generateMeme: (prompt, style = 'viral') => 
    api.post('/marketing/meme', { prompt, style }),
  postToTwitter: (content, mediaUrl = null) => 
    api.post('/marketing/twitter', { content, media_url: mediaUrl }),
};

// Strategy endpoints
export const strategyAPI = {
  getAIReasoning: (prompt) => api.post('/strategy/reasoning', { prompt }),
};

export default api;
