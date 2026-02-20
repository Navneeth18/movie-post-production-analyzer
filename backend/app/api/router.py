from fastapi import APIRouter
from app.api.endpoints import analytics, calculator, marketing, strategy, auth, movies, release_strategy

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(release_strategy.router, prefix="/release-strategy", tags=["release-strategy"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(calculator.router, prefix="/calculator", tags=["calculator"])
api_router.include_router(marketing.router, prefix="/marketing", tags=["marketing"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
