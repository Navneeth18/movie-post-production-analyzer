from typing import List, Dict
from datetime import datetime, timedelta

class ReleaseStrategyService:
    
    @staticmethod
    def categorize_movie(movie: dict) -> str:
        """
        Categorize movie as big, medium, or small based on budget and cast score.
        """
        budget = movie.get("budget", 0)
        cast_score = movie.get("cast_score", 0)
        
        # Budget thresholds in INR (crores)
        if budget >= 50_000_000:  # 5 Cr+
            if cast_score >= 75:
                return "big"
            else:
                return "medium"
        elif budget >= 15_000_000:  # 1.5 Cr+
            if cast_score >= 70:
                return "medium"
            else:
                return "small"
        else:
            return "small"
    
    @staticmethod
    def calculate_threat_level(your_movie: dict, competitor: dict, days_diff: int) -> str:
        """
        Calculate competitive threat level based on multiple factors.
        """
        # Same genre = higher threat
        genre_match = your_movie.get("genre") == competitor.get("genre")
        
        # Same language/region = higher threat
        language_match = your_movie.get("language") == competitor.get("language")
        region_overlap = your_movie.get("region") == competitor.get("region")
        
        # Category comparison
        your_category = ReleaseStrategyService.categorize_movie(your_movie)
        comp_category = ReleaseStrategyService.categorize_movie(competitor)
        
        # Score comparison
        your_total = (
            your_movie.get("cast_score", 0) * 0.4 +
            your_movie.get("historic_score", 0) * 0.3 +
            your_movie.get("public_pulse_score", 0) * 0.3
        )
        comp_total = (
            competitor.get("cast_score", 0) * 0.4 +
            competitor.get("historic_score", 0) * 0.3 +
            competitor.get("public_pulse_score", 0) * 0.3
        )
        
        threat_score = 0
        
        # Date proximity (within 7 days = high threat)
        if days_diff <= 7:
            threat_score += 3
        elif days_diff <= 14:
            threat_score += 2
        elif days_diff <= 21:
            threat_score += 1
        
        # Genre match
        if genre_match:
            threat_score += 2
        
        # Language/region match
        if language_match:
            threat_score += 2
        if region_overlap:
            threat_score += 1
        
        # Competitor is bigger category
        if comp_category == "big" and your_category != "big":
            threat_score += 2
        elif comp_category == "medium" and your_category == "small":
            threat_score += 1
        
        # Competitor has higher scores
        if comp_total > your_total + 10:
            threat_score += 2
        elif comp_total > your_total:
            threat_score += 1
        
        # Determine threat level
        if threat_score >= 7:
            return "high"
        elif threat_score >= 4:
            return "medium"
        else:
            return "low"
    
    @staticmethod
    def generate_date_range_analysis(
        movie: dict,
        competitors: List,
        target_date: datetime
    ) -> Dict:
        """
        Generate comprehensive analysis of the release date range.
        """
        high_threats = [c for c in competitors if c.threat_level == "high"]
        big_movies = [c for c in competitors if c.category == "big"]
        
        # Find optimal windows (gaps with no high threats)
        optimal_windows = []
        
        # Check week before and after target
        week_before = target_date - timedelta(days=7)
        week_after = target_date + timedelta(days=7)
        
        competitors_in_week = [
            c for c in competitors 
            if week_before <= c.release_date <= week_after
        ]
        
        if not competitors_in_week:
            optimal_windows.append({
                "start_date": week_before,
                "end_date": week_after,
                "reason": "Clear window with no direct competition"
            })
        
        # Generate recommendation
        if len(high_threats) == 0:
            recommendation = f"Good release window. No high-threat competitors detected. Proceed with {target_date.strftime('%B %d, %Y')}."
        elif len(high_threats) == 1:
            threat = high_threats[0]
            recommendation = f"Moderate risk. {threat.title} ({threat.category} movie) releases {threat.days_from_your_release} days away. Consider differentiated marketing."
        else:
            recommendation = f"High risk window. {len(high_threats)} high-threat competitors detected. Strongly consider alternative dates."
        
        # Risk assessment
        if len(big_movies) >= 2:
            risk = "HIGH - Multiple big-budget films in range"
        elif len(high_threats) >= 2:
            risk = "HIGH - Multiple direct competitors"
        elif len(high_threats) == 1:
            risk = "MEDIUM - One significant competitor"
        else:
            risk = "LOW - Favorable competitive landscape"
        
        return {
            "recommendation": recommendation,
            "optimal_windows": optimal_windows,
            "risk_assessment": risk
        }
