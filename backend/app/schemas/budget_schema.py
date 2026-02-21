"""
Budget Planning Schemas
"""
from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime

class BudgetAllocations(BaseModel):
    """Channel allocation percentages"""
    digital: float = Field(default=30, ge=0, le=100)
    traditional: float = Field(default=15, ge=0, le=100)
    influencer: float = Field(default=20, ge=0, le=100)
    events: float = Field(default=10, ge=0, le=100)
    pr: float = Field(default=15, ge=0, le=100)
    contingency: float = Field(default=10, ge=0, le=100)

class BudgetPlanCreate(BaseModel):
    """Create or update budget plan"""
    total_budget: float = Field(gt=0, description="Total marketing budget in INR")
    allocations: BudgetAllocations
    timeline_weeks: int = Field(default=8, ge=4, le=16, description="Weeks before release")

class BudgetPlanResponse(BaseModel):
    """Budget plan response"""
    id: str
    movie_id: str
    producer_id: str
    total_budget: float
    allocations: BudgetAllocations
    timeline_weeks: int
    total_allocated_percentage: float
    projected_roi: float
    projected_revenue: float
    created_at: datetime
    updated_at: datetime

class BudgetOptimizationRequest(BaseModel):
    """Request AI optimization"""
    movie_title: str
    genre: str
    budget: float
    total_marketing_budget: float
    timeline_weeks: int
    current_allocations: BudgetAllocations
