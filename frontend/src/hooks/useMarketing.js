import { useState } from 'react';
import { marketingAPI } from '../services/api';

export const useMarketing = () => {
  const [loading, setLoading] = useState(false);
  const [meme, setMeme] = useState(null);
  const [tweetResult, setTweetResult] = useState(null);

  const generateMeme = async (prompt, style = 'viral') => {
    setLoading(true);
    try {
      const response = await marketingAPI.generateMeme(prompt, style);
      setMeme(response.data);
      return response.data;
    } catch (error) {
      console.error('Meme generation failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const postToTwitter = async (content, mediaUrl = null) => {
    setLoading(true);
    try {
      const response = await marketingAPI.postToTwitter(content, mediaUrl);
      setTweetResult(response.data);
      return response.data;
    } catch (error) {
      console.error('Twitter post failed:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { loading, meme, tweetResult, generateMeme, postToTwitter };
};
