"""
YouTube Sentiment Analysis Service
Analyzes YouTube video comments, likes, dislikes to calculate public pulse score
"""
from typing import Optional, Dict, List
import re
import os

class YouTubeSentimentService:
    """Service for analyzing YouTube data to calculate public pulse"""
    
    @staticmethod
    def extract_video_id(youtube_url: str) -> Optional[str]:
        """
        Extract video ID from various YouTube URL formats
        
        Supports:
        - https://www.youtube.com/watch?v=VIDEO_ID
        - https://youtu.be/VIDEO_ID
        - https://www.youtube.com/embed/VIDEO_ID
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, youtube_url)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def calculate_public_pulse(
        title: str,
        youtube_video_id: Optional[str] = None,
        likes: int = 0,
        dislikes: int = 0,
        views: int = 0,
        comments: list = None
    ) -> float:
        """
        Calculate public pulse score based on YouTube metrics
        
        Args:
            title: Movie title
            youtube_video_id: YouTube video ID (trailer)
            likes: Number of likes
            dislikes: Number of dislikes
            views: Number of views
            comments: List of top comments
            
        Returns:
            float: Public pulse score (0-100)
        """
        
        # Base score
        score = 50.0
        
        # 1. Like/Dislike Ratio (30% weight)
        if likes > 0 or dislikes > 0:
            total_reactions = likes + dislikes
            like_ratio = likes / total_reactions if total_reactions > 0 else 0.5
            like_score = like_ratio * 100
            score += (like_score - 50) * 0.3
        
        # 2. Engagement Rate (20% weight)
        if views > 0:
            engagement_rate = (likes + dislikes) / views
            # Good engagement is typically 3-5%
            engagement_score = min(engagement_rate / 0.05 * 100, 100)
            score += (engagement_score - 50) * 0.2
        
        # 3. Comment Sentiment (50% weight)
        if comments:
            sentiment_score = YouTubeSentimentService._analyze_comments_sentiment(comments)
            score += (sentiment_score - 50) * 0.5
        
        # Ensure score is between 0 and 100
        return max(0, min(score, 100))
    
    @staticmethod
    def _analyze_comments_sentiment(comments: list) -> float:
        """
        Analyze sentiment of comments using simple keyword-based approach
        
        For production, this should use a transformer model like:
        - distilbert-base-uncased-finetuned-sst-2-english
        - cardiffnlp/twitter-roberta-base-sentiment
        
        Args:
            comments: List of comment texts
            
        Returns:
            float: Sentiment score (0-100)
        """
        
        if not comments:
            return 50.0
        
        # Positive keywords
        positive_keywords = [
            'amazing', 'awesome', 'great', 'excellent', 'fantastic', 'wonderful',
            'love', 'best', 'perfect', 'brilliant', 'outstanding', 'superb',
            'excited', 'waiting', 'can\'t wait', 'masterpiece', 'blockbuster',
            'goosebumps', 'fire', '🔥', '❤️', '👏', '💯'
        ]
        
        # Negative keywords
        negative_keywords = [
            'bad', 'worst', 'terrible', 'awful', 'horrible', 'disappointing',
            'waste', 'boring', 'poor', 'flop', 'disaster', 'pathetic',
            'overrated', 'cringe', 'skip', 'avoid', '👎', '😴'
        ]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for comment in comments[:10]:  # Analyze top 10 comments
            comment_lower = comment.lower()
            
            pos_matches = sum(1 for keyword in positive_keywords if keyword in comment_lower)
            neg_matches = sum(1 for keyword in negative_keywords if keyword in comment_lower)
            
            if pos_matches > neg_matches:
                positive_count += 1
            elif neg_matches > pos_matches:
                negative_count += 1
            else:
                neutral_count += 1
        
        total = positive_count + negative_count + neutral_count
        if total == 0:
            return 50.0
        
        # Calculate sentiment score
        positive_ratio = positive_count / total
        negative_ratio = negative_count / total
        
        # Score: 0-100 where 50 is neutral
        sentiment_score = 50 + (positive_ratio * 50) - (negative_ratio * 50)
        
        return max(0, min(sentiment_score, 100))
    
    @staticmethod
    async def fetch_youtube_data(video_id: str) -> Dict:
        """
        Fetch YouTube video data using YouTube Data API
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            dict: Video data including likes, dislikes, views, comments
        """
        
        try:
            # Try to use YouTube Data API if available
            from googleapiclient.discovery import build
            from googleapiclient.errors import HttpError
            
            api_key = os.getenv('YOUTUBE_API_KEY')
            if not api_key:
                # Return mock data if no API key
                return YouTubeSentimentService._get_mock_youtube_data()
            
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Get video statistics
            video_response = youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                return YouTubeSentimentService._get_mock_youtube_data()
            
            video_stats = video_response['items'][0]['statistics']
            
            # Get top comments
            try:
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    maxResults=10,
                    order='relevance'
                ).execute()
                
                comments = [
                    item['snippet']['topLevelComment']['snippet']['textDisplay']
                    for item in comments_response.get('items', [])
                ]
            except HttpError:
                # Comments might be disabled
                comments = []
            
            return {
                'likes': int(video_stats.get('likeCount', 0)),
                'dislikes': 0,  # YouTube removed dislike count
                'views': int(video_stats.get('viewCount', 0)),
                'comments': comments,
                'comment_count': int(video_stats.get('commentCount', 0))
            }
            
        except ImportError:
            # google-api-python-client not installed
            return YouTubeSentimentService._get_mock_youtube_data()
        except Exception as e:
            print(f"Error fetching YouTube data: {e}")
            return YouTubeSentimentService._get_mock_youtube_data()
    
    @staticmethod
    def _get_mock_youtube_data() -> Dict:
        """Return mock YouTube data for testing"""
        return {
            'likes': 15000,
            'dislikes': 500,
            'views': 500000,
            'comments': [
                'This looks amazing! Can\'t wait to watch it! 🔥',
                'The trailer gave me goosebumps! Definitely watching this',
                'Great cast and direction. This will be a blockbuster',
                'Excited for this release! ❤️',
                'The cinematography looks stunning',
                'Not impressed with the trailer',
                'Looks like another typical movie',
                'Hope the movie is better than the trailer',
                'Waiting for this masterpiece! 💯',
                'This is going to be epic! 👏'
            ],
            'comment_count': 2500
        }
    
    @staticmethod
    def calculate_hws_score(
        cast_score: float,
        historic_score: float,
        public_pulse_score: float
    ) -> float:
        """
        Calculate Hit-Worthiness Score (HWS)
        
        Formula: HWS = (Cast * 0.4) + (Historic * 0.3) + (Pulse * 0.3)
        
        Args:
            cast_score: Cast star power score (0-100)
            historic_score: Director/genre historic performance (0-100)
            public_pulse_score: Public sentiment score (0-100)
            
        Returns:
            float: HWS score (0-100)
        """
        
        hws = (
            cast_score * 0.4 +
            historic_score * 0.3 +
            public_pulse_score * 0.3
        )
        
        return round(hws, 2)
