from typing import List, Optional
from datetime import datetime

class MovieService:
    @staticmethod
    def calculate_cast_score(cast: List[dict]) -> float:
        """Calculate cast score based on star power"""
        if not cast:
            return 50.0
        
        total_star_power = sum(member.get('star_power', 50) for member in cast)
        avg_star_power = total_star_power / len(cast)
        return min(avg_star_power, 100.0)
    
    @staticmethod
    def calculate_historic_score(director: str, genre: str) -> float:
        """Calculate historic score based on director and genre performance"""
        # Placeholder logic - should query historical data
        base_score = 60.0
        
        # Director reputation boost (would come from database)
        director_boost = 10.0
        
        # Genre performance (would come from market data)
        genre_multiplier = 1.1 if genre in ["Drama", "Thriller"] else 1.0
        
        return min((base_score + director_boost) * genre_multiplier, 100.0)
    
    @staticmethod
    async def calculate_public_pulse(title: str, themes: str) -> float:
        """Calculate public pulse score based on social media sentiment"""
        # Placeholder - would integrate with scraper service
        base_pulse = 55.0
        
        # Theme relevance boost
        trending_themes = ["family", "social", "thriller", "crime"]
        theme_boost = 5.0 if any(t in themes.lower() for t in trending_themes) else 0
        
        return min(base_pulse + theme_boost, 100.0)
    
    @staticmethod
    def compare_movies(movie1: dict, movie2: dict) -> dict:
        """Compare two movies and determine which is stronger"""
        m1_total = (
            movie1.get('cast_score', 0) * 0.4 +
            movie1.get('historic_score', 0) * 0.3 +
            movie1.get('public_pulse_score', 0) * 0.3
        )
        
        m2_total = (
            movie2.get('cast_score', 0) * 0.4 +
            movie2.get('historic_score', 0) * 0.3 +
            movie2.get('public_pulse_score', 0) * 0.3
        )
        
        diff = abs(m1_total - m2_total)
        
        if diff < 5:
            strength = "equal"
            recommendation = "Both films are evenly matched. Consider differentiated marketing strategies."
        elif m1_total > m2_total:
            strength = "stronger"
            recommendation = f"Your film is stronger by {diff:.1f} points. Capitalize on this advantage with aggressive marketing."
        else:
            strength = "weaker"
            recommendation = f"Competitor is stronger by {diff:.1f} points. Consider adjusting release date or focusing on niche marketing."
        
        return {
            "overall_strength": strength,
            "recommendation": recommendation,
            "your_total_score": m1_total,
            "competitor_total_score": m2_total
        }
    
    @staticmethod
    def calculate_release_date_proximity(date1: Optional[datetime], date2: Optional[datetime]) -> int:
        """Calculate days between two release dates"""
        if not date1 or not date2:
            return 999  # Large number if dates not set
        
        delta = abs((date1 - date2).days)
        return delta
