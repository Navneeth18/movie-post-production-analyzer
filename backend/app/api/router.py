from fastapi import APIRouter
from app.api.endpoints import analytics, calculator, marketing, strategy, auth, movies, release_strategy, public_pulse, facebook_campaign, budget, data_analytics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(public_pulse.router, prefix="/public-pulse", tags=["public-pulse"])
api_router.include_router(facebook_campaign.router, prefix="/facebook-campaign", tags=["facebook-campaign"])
api_router.include_router(release_strategy.router, prefix="/release-strategy", tags=["release-strategy"])
api_router.include_router(budget.router, prefix="/budget", tags=["budget"])
api_router.include_router(data_analytics.router, prefix="/data-analytics", tags=["data-analytics"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(calculator.router, prefix="/calculator", tags=["calculator"])
api_router.include_router(marketing.router, prefix="/marketing", tags=["marketing"])
api_router.include_router(strategy.router, prefix="/strategy", tags=["strategy"])
