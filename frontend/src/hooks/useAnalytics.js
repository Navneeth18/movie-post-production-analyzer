import { useState } from 'react';
import { analyticsAPI } from '../services/api';

export const useAnalytics = () => {
  const [sentiment, setSentiment] = useState(null);
  const [pulse, setPulse] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSentiment = async (query) => {
    setLoading(true);
    try {
      const response = await analyticsAPI.getSentiment(query);
      setSentiment(response.data);
    } catch (error) {
      console.error('Sentiment fetch failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPulse = async (query) => {
    setLoading(true);
    try {
      const response = await analyticsAPI.getPulse(query);
      setPulse(response.data);
    } catch (error) {
      console.error('Pulse fetch failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return { sentiment, pulse, loading, fetchSentiment, fetchPulse };
};
