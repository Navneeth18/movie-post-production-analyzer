from pydantic import BaseModel, Field

class HWSRequest(BaseModel):
    hero: str = Field(..., example="Prabhas")
    director: str = Field(..., example="S. S. Rajamouli")
    heroine: str = Field(..., example="Anushka Shetty")
    producer: str = Field(..., example="Arka Media Works")
    genre_score: float = Field(..., ge=0, le=100, description="Current trend score for the genre")
    popularity_score: float = Field(..., ge=0, le=100)
    expected_imdb: float = Field(..., ge=0, le=10)

class HWSResponse(BaseModel):
    hws_score: float
    category: str
    risk_level: str
    recommendation: str