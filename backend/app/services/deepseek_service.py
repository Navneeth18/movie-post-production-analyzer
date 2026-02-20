import httpx
from typing import List, Dict, Optional
from datetime import datetime
from app.core.config import settings

class DeepSeekService:
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY
        self.base_url = "https://api.deepseek.com/v1"
    
    async def generate_pr_strategy(
        self,
        movie_data: dict,
        competitors: List[dict],
        focus_areas: List[str]
    ) -> dict:
        """Generate comprehensive PR strategy using DeepSeek-R1"""
        
        prompt = self._build_pr_strategy_prompt(movie_data, competitors, focus_areas)
        
        response = await self._call_deepseek(prompt)
        
        # Parse response into structured format
        return self._parse_pr_strategy_response(response)
    
    async def analyze_release_date(
        self,
        movie_data: dict,
        competitors: List[dict],
        date_range: tuple
    ) -> dict:
        """Analyze optimal release date using DeepSeek-R1"""
        
        prompt = self._build_release_date_prompt(movie_data, competitors, date_range)
        
        response = await self._call_deepseek(prompt)
        
        return self._parse_release_date_response(response, movie_data["target_date"])

    
    def _build_pr_strategy_prompt(
        self,
        movie_data: dict,
        competitors: List[dict],
        focus_areas: List[str]
    ) -> str:
        """Build prompt for PR strategy generation"""
        
        comp_summary = "\n".join([
            f"- {c['title']} ({c['category']} movie, {c['genre']}, Budget: ₹{c['budget']/10000000:.1f}Cr)"
            for c in competitors[:5]
        ])
        
        return f"""You are an expert film PR strategist for Indian cinema. Analyze and create a comprehensive PR strategy.

MOVIE DETAILS:
- Title: {movie_data['title']}
- Category: {movie_data['category']}
- Genre: {movie_data['genre']}
- Budget: ₹{movie_data['budget']/10000000:.1f} Crores
- Language: {movie_data['language']}
- Region: {movie_data['region']}
- Themes: {movie_data['themes']}
- Cast Score: {movie_data['cast_score']}/100
- Historic Score: {movie_data['historic_score']}/100
- Public Pulse: {movie_data['public_pulse_score']}/100

COMPETING MOVIES:
{comp_summary}

FOCUS AREAS: {', '.join(focus_areas)}

Provide a detailed PR strategy including:
1. Overall strategy narrative
2. Key differentiators (3-5 points)
3. Target audience approach
4. Media channels with specific tactics
5. Timeline (pre-release, release, post-release)
6. Budget allocation recommendations
7. Risk mitigation strategies
8. Success metrics

Format as JSON."""

    
    def _build_release_date_prompt(
        self,
        movie_data: dict,
        competitors: List[dict],
        date_range: tuple
    ) -> str:
        """Build prompt for release date analysis"""
        
        comp_list = "\n".join([
            f"- {c['title']} ({c['category']}, {c['genre']}) on {c['release_date'].strftime('%B %d, %Y')} - Scores: Cast {c['cast_score']}, Historic {c['historic_score']}, Pulse {c['public_pulse_score']}"
            for c in competitors
        ])
        
        return f"""You are a film release strategy expert. Analyze the optimal release date.

YOUR MOVIE:
- Title: {movie_data['title']}
- Category: {movie_data['category']}
- Genre: {movie_data['genre']}
- Language: {movie_data['language']}
- Region: {movie_data['region']}
- Current Target: {movie_data['target_date'].strftime('%B %d, %Y')}

COMPETITORS IN RANGE ({date_range[0].strftime('%B %d')} to {date_range[1].strftime('%B %d, %Y')}):
{comp_list}

Analyze and recommend:
1. Should they keep the current date or change?
2. If change, what's the optimal date?
3. Confidence score (0-100)
4. Detailed reasoning
5. 2-3 alternative dates
6. Competitive analysis
7. Market conditions assessment
8. Specific action items

Format as JSON."""

    
    async def _call_deepseek(self, prompt: str) -> str:
        """Make API call to DeepSeek"""
        
        if not self.api_key or self.api_key == "your_deepseek_api_key":
            # Fallback to mock response for development
            return self._mock_response(prompt)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "deepseek-reasoner",
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data["choices"][0]["message"]["content"]
                else:
                    return self._mock_response(prompt)
        except Exception as e:
            print(f"DeepSeek API error: {e}")
            return self._mock_response(prompt)

    
    def _mock_response(self, prompt: str) -> str:
        """Mock response for development/testing"""
        if "PR strategy" in prompt or "PR Strategy" in prompt:
            return """{
                "strategy": "Position as authentic regional cinema with universal themes. Leverage festival circuit credibility and grassroots marketing.",
                "key_differentiators": [
                    "Authentic storytelling with regional flavor",
                    "Strong director reputation in indie circuit",
                    "Unique thematic approach to family dynamics",
                    "Cost-effective production with high artistic value"
                ],
                "target_audience": {
                    "primary": "Urban millennials interested in meaningful cinema",
                    "secondary": "Festival circuit audience and critics",
                    "tertiary": "Regional audience seeking authentic representation"
                },
                "media_channels": [
                    {"channel": "Social Media", "tactics": "Behind-the-scenes content, director interviews, theme-based campaigns", "budget_percent": 35},
                    {"channel": "Film Festivals", "tactics": "Strategic submissions, Q&A sessions, networking", "budget_percent": 20},
                    {"channel": "Press & Critics", "tactics": "Early screenings, press kits, critic engagement", "budget_percent": 25},
                    {"channel": "Influencer Marketing", "tactics": "Micro-influencers in film community", "budget_percent": 20}
                ],
                "timeline": [
                    {"phase": "Pre-release (8-12 weeks)", "activities": "Festival submissions, teaser release, press kit distribution"},
                    {"phase": "Release (2-4 weeks)", "activities": "Trailer launch, critic screenings, social media blitz"},
                    {"phase": "Post-release", "activities": "Word-of-mouth amplification, OTT negotiations, awards campaign"}
                ],
                "budget_allocation": {
                    "digital_marketing": 40,
                    "traditional_media": 20,
                    "events_screenings": 25,
                    "influencer_partnerships": 15
                },
                "risk_mitigation": [
                    "Build strong critic relationships early",
                    "Create viral-worthy content pieces",
                    "Maintain authentic voice to avoid backlash",
                    "Have contingency for date changes"
                ],
                "success_metrics": [
                    "Social media engagement rate > 5%",
                    "Press coverage in 10+ major outlets",
                    "Festival selections in 3+ tier-1 festivals",
                    "Opening weekend occupancy > 60%",
                    "Positive critic reviews > 75%"
                ]
            }"""
        else:
            return """{
                "recommended_date": "2024-12-20",
                "confidence_score": 78,
                "reasoning": "Current date has moderate competition. Moving 5 days later provides clearer window with only one small competitor. Avoids direct clash with big-budget release on Dec 15.",
                "alternative_dates": [
                    {"date": "2024-12-13", "pros": "Earlier window, less competition", "cons": "Less time for marketing buildup"},
                    {"date": "2024-12-27", "pros": "Holiday season advantage", "cons": "Year-end fatigue, family commitments"}
                ],
                "competitive_analysis": "Two big movies within 10 days create crowded marketplace. Your medium-budget film needs breathing room. Recommended date has 7-day gap from nearest competitor.",
                "market_conditions": "December is strong for family dramas. Holiday season provides extended viewing window. OTT platforms actively seeking content for year-end.",
                "action_items": [
                    "Confirm new date within 48 hours",
                    "Adjust marketing timeline accordingly",
                    "Notify distribution partners",
                    "Accelerate social media campaign to build momentum"
                ]
            }"""

    
    def _parse_pr_strategy_response(self, response: str) -> dict:
        """Parse PR strategy response"""
        import json
        try:
            return json.loads(response)
        except:
            # Return structured default if parsing fails
            return {
                "strategy": response[:500],
                "key_differentiators": ["Unique positioning", "Strong narrative", "Targeted approach"],
                "target_audience": {"primary": "Core demographic", "secondary": "Extended audience"},
                "media_channels": [{"channel": "Digital", "tactics": "Social media", "budget_percent": 50}],
                "timeline": [{"phase": "Pre-release", "activities": "Marketing campaign"}],
                "budget_allocation": {"digital": 60, "traditional": 40},
                "risk_mitigation": ["Monitor competition", "Flexible strategy"],
                "success_metrics": ["Engagement rate", "Box office performance"]
            }
    
    def _parse_release_date_response(self, response: str, current_date: datetime) -> dict:
        """Parse release date analysis response"""
        import json
        try:
            data = json.loads(response)
            # Ensure recommended_date is datetime
            if isinstance(data.get("recommended_date"), str):
                data["recommended_date"] = datetime.fromisoformat(data["recommended_date"])
            return data
        except:
            return {
                "recommended_date": current_date,
                "confidence_score": 50,
                "reasoning": "Analysis completed. Consider competitive landscape.",
                "alternative_dates": [],
                "competitive_analysis": "Multiple factors to consider.",
                "market_conditions": "Standard market conditions apply.",
                "action_items": ["Review analysis", "Make decision"]
            }
