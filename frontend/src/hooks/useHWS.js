import { useState, useEffect } from 'react';
import { calculatorAPI } from '../services/api';

export const useHWS = (filmData) => {
  const [hwsScore, setHwsScore] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const calculateHWS = async (scores) => {
    setLoading(true);
    setError(null);
    try {
      const response = await calculatorAPI.calculateHWS(scores);
      setHwsScore(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return { hwsScore, loading, error, calculateHWS };
};
