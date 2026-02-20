from fastapi import APIRouter
from app.services.hws_service import HWSService

router = APIRouter()

@router.post("/hws")
def calculate_hws():
    """Calculate HWS score for a movie"""
    # Example calculation
    hws_score = HWSService.calculate_hws(
        director=80, historical=70, sentiment=65,
        pulse=70, genre=60, budget=50, timing=75
    )
    category = HWSService.get_category(hws_score)
    
    return {
        "hws_score": hws_score,
        "category": category,
        "message": "HWS score calculated successfully"
    }
