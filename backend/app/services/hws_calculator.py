"""
Historical Weighted Score (HWS) Calculator
Uses exponential scaling and market-adjusted weights for accurate movie categorization
"""
from typing import Dict, List, Optional
from app.db.mongodb import get_database

class HWSCalculator:
    """
    Calculate Historical Weighted Score using exponential grading
    
    Formula:
    HWS = (W_d × S_d) + (W_h × S_h) + (W_g × S_g) + (W_v × S_v) + 
          (W_i × S_i) + (W_f × S_f) + (W_p × S_p)
    """
    
    # Weights (Market Impact)
    WEIGHTS = {
        'director': 0.25,      # 25% - Director's brand is primary trust factor
        'genre': 0.20,         # 20% - Trending genre has higher audience floor
        'hero': 0.15,          # 15% - Initial 3-day theatrical opening pull
        'popularity': 0.15,    # 15% - Real-time interest (Pulse metric)
        'predicted_imdb': 0.10,  # 10% - Long-term OTT value
        'heroine': 0.08,       # 8% - Chemistry and visual appeal
        'producer': 0.07       # 7% - Resources for distribution and scale
    }
    
    # Exponential Grading Scale
    GRADE_SCORES = {
        'Grade 1': 100,  # Elite
        'Grade 2': 40,   # Established
        'Grade 3': 10    # Newcomer/Budding
    }
    
    # Genre Trending Scores (can be updated based on market trends)
    GENRE_SCORES = {
        'Action': 90,
        'Thriller': 85,
        'Drama': 70,
        'Comedy': 75,
        'Romance': 65,
        'Horror': 80,
        'Sci-Fi': 75,
        'Fantasy': 70,
        'Crime': 80,
        'Mystery': 75
    }
    
    @staticmethod
    async def get_artist_grade(name: str, role: str) -> str:
        """
        Get artist grade from database
        
        Args:
            name: Artist name
            role: Artist role (Director, Hero, Heroine, Producer)
            
        Returns:
            str: Grade (Grade 1, Grade 2, or Grade 3)
        """
        db = get_database()
        
        # Map role to database role names
        role_mapping = {
            'Director': 'Director',
            'Hero': 'Lead 1 (Hero)',
            'Heroine': 'Lead 2 (Heroine)',
            'Producer': 'Producer'
        }
        
        db_role = role_mapping.get(role, role)
        
        # Search for artist in database
        artist = await db.artists.find_one({
            "Name": {"$regex": name, "$options": "i"},
            "Role": db_role
        })
        
        if artist:
            return artist.get('Grade', 'Grade 3')
        
        # Default to Grade 3 if not found
        return 'Grade 3'
    
    @staticmethod
    def grade_to_score(grade: str) -> float:
        """Convert grade to exponential score"""
        return HWSCalculator.GRADE_SCORES.get(grade, 10)
    
    @staticmethod
    def genre_to_score(genres: List[str]) -> float:
        """
        Calculate genre score based on trending genres
        Takes the highest scoring genre from the list
        """
        if not genres:
            return 50.0
        
        scores = [HWSCalculator.GENRE_SCORES.get(genre, 50) for genre in genres]
        return max(scores)
    
    @staticmethod
    async def calculate_director_score(director_name: str) -> float:
        """Calculate director score (S_d)"""
        grade = await HWSCalculator.get_artist_grade(director_name, 'Director')
        return HWSCalculator.grade_to_score(grade)
    
    @staticmethod
    async def calculate_hero_score(cast: List[dict]) -> float:
        """Calculate hero/lead score (S_h)"""
        # Find hero in cast
        hero = next((c for c in cast if c.get('role', '').lower() in ['hero', 'lead', 'actor']), None)
        
        if not hero:
            return 10.0  # Default Grade 3 score
        
        grade = await HWSCalculator.get_artist_grade(hero['name'], 'Hero')
        return HWSCalculator.grade_to_score(grade)
    
    @staticmethod
    async def calculate_heroine_score(cast: List[dict]) -> float:
        """Calculate heroine/lead 2 score (S_f)"""
        # Find heroine in cast
        heroine = next((c for c in cast if c.get('role', '').lower() in ['heroine', 'actress', 'lead actress']), None)
        
        if not heroine:
            return 10.0  # Default Grade 3 score
        
        grade = await HWSCalculator.get_artist_grade(heroine['name'], 'Heroine')
        return HWSCalculator.grade_to_score(grade)
    
    @staticmethod
    async def calculate_producer_score(producer_name: str) -> float:
        """Calculate producer score (S_p)"""
        grade = await HWSCalculator.get_artist_grade(producer_name, 'Producer')
        return HWSCalculator.grade_to_score(grade)
    
    @staticmethod
    def calculate_predicted_imdb(director_score: float, genre_score: float) -> float:
        """
        Calculate predicted IMDb score (S_i)
        Based on director's historical average and genre performance
        """
        # Weighted average: 70% director, 30% genre
        predicted = (director_score * 0.7) + (genre_score * 0.3)
        return predicted
    
    @staticmethod
    async def calculate_hws(
        director: str,
        genres: List[str],
        cast: List[dict],
        producer: Optional[str] = None,
        popularity_score: float = 50.0
    ) -> Dict:
        """
        Calculate complete HWS score
        
        Args:
            director: Director name
            genres: List of genres
            cast: List of cast members with name and role
            producer: Producer name (optional)
            popularity_score: Public pulse score (0-100)
            
        Returns:
            dict: HWS score and breakdown
        """
        
        # Calculate individual scores
        S_d = await HWSCalculator.calculate_director_score(director)
        S_h = await HWSCalculator.calculate_hero_score(cast)
        S_f = await HWSCalculator.calculate_heroine_score(cast)
        S_g = HWSCalculator.genre_to_score(genres)
        S_v = popularity_score  # Pulse metric
        S_i = HWSCalculator.calculate_predicted_imdb(S_d, S_g)
        S_p = await HWSCalculator.calculate_producer_score(producer) if producer else 10.0
        
        # Apply weights
        W = HWSCalculator.WEIGHTS
        
        hws = (
            (W['director'] * S_d) +
            (W['hero'] * S_h) +
            (W['genre'] * S_g) +
            (W['popularity'] * S_v) +
            (W['predicted_imdb'] * S_i) +
            (W['heroine'] * S_f) +
            (W['producer'] * S_p)
        )
        
        # Determine category
        if hws >= 75:
            category = "BIG"
            market_action = "Global theatrical release; Massive marketing spend"
        elif hws >= 45:
            category = "MEDIUM"
            market_action = "Targeted regional release; High PR influencer focus"
        else:
            category = "SMALL"
            market_action = "OTT-First strategy or hyper-niche community marketing"
        
        return {
            'hws_score': round(hws, 2),
            'category': category,
            'market_action': market_action,
            'breakdown': {
                'director_score': round(S_d, 2),
                'director_contribution': round(W['director'] * S_d, 2),
                'hero_score': round(S_h, 2),
                'hero_contribution': round(W['hero'] * S_h, 2),
                'heroine_score': round(S_f, 2),
                'heroine_contribution': round(W['heroine'] * S_f, 2),
                'genre_score': round(S_g, 2),
                'genre_contribution': round(W['genre'] * S_g, 2),
                'popularity_score': round(S_v, 2),
                'popularity_contribution': round(W['popularity'] * S_v, 2),
                'predicted_imdb': round(S_i, 2),
                'predicted_imdb_contribution': round(W['predicted_imdb'] * S_i, 2),
                'producer_score': round(S_p, 2),
                'producer_contribution': round(W['producer'] * S_p, 2)
            }
        }
    
    @staticmethod
    async def calculate_historical_movie_hws(
        director: str,
        genre: str,
        hero: Optional[str] = None,
        heroine: Optional[str] = None,
        producer: Optional[str] = None,
        budget: float = 0,
        revenue: float = 0
    ) -> Dict:
        """
        Calculate HWS for historical movies
        Uses actual performance data to estimate popularity score
        """
        
        # Create cast list from hero/heroine
        cast = []
        if hero:
            cast.append({'name': hero, 'role': 'Hero'})
        if heroine:
            cast.append({'name': heroine, 'role': 'Heroine'})
        
        # Estimate popularity score from budget/revenue
        if budget > 0 and revenue > 0:
            roi = (revenue - budget) / budget
            # Convert ROI to 0-100 scale
            popularity_score = min(50 + (roi * 50), 100)
        else:
            popularity_score = 50.0
        
        # Calculate HWS
        return await HWSCalculator.calculate_hws(
            director=director,
            genres=[genre] if genre else [],
            cast=cast,
            producer=producer,
            popularity_score=popularity_score
        )
