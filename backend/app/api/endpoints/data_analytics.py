"""
Data Analytics API Endpoints
Provides advanced analytics and visualizations
"""
from fastapi import APIRouter, HTTPException
from app.services.data_analytics_service import DataAnalyticsService

router = APIRouter()

@router.get("/grade-performance")
async def get_grade_performance():
    """
    Get grade-performance correlation data
    Box plot showing IMDB rating distributions by director grade
    """
    try:
        service = DataAnalyticsService()
        result = service.get_grade_performance_data()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/genre-timeline")
async def get_genre_timeline():
    """
    Get genre popularity over time
    Time-series data showing popularity per genre per quarter
    """
    try:
        service = DataAnalyticsService()
        result = service.get_genre_popularity_timeline()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/talent-matrix")
async def get_talent_matrix():
    """
    Get talent value matrix
    Scatter plot data for hero performance (IMDB vs Popularity)
    """
    try:
        service = DataAnalyticsService()
        result = service.get_talent_value_matrix()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demographic-heatmap")
async def get_demographic_heatmap():
    """
    Get demographic heatmap data
    Genre-age group correlation based on popularity
    """
    try:
        service = DataAnalyticsService()
        result = service.get_demographic_heatmap()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all")
async def get_all_analytics():
    """
    Get all analytics data at once
    Returns all four visualizations data
    """
    try:
        service = DataAnalyticsService()
        result = service.get_all_analytics()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
