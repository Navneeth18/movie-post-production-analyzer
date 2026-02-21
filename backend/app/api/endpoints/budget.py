"""
Budget Planning API Endpoints
Handles marketing budget allocation and optimization
"""
from fastapi import APIRouter, HTTPException, Depends, status
from bson import ObjectId
from datetime import datetime
from typing import Optional
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.schemas.budget_schema import (
    BudgetPlanCreate,
    BudgetPlanResponse,
    BudgetAllocations,
    BudgetOptimizationRequest
)
from app.services.ai_service import AIService
from app.core.config import settings

router = APIRouter()

# Channel ROI data
CHANNEL_ROI = {
    "digital": 3.2,
    "traditional": 1.8,
    "influencer": 2.5,
    "events": 2.0,
    "pr": 2.8,
    "contingency": 0.0
}

def calculate_projected_roi(total_budget: float, allocations: BudgetAllocations) -> tuple[float, float]:
    """Calculate projected ROI and revenue"""
    allocations_dict = allocations.dict()
    total_revenue = 0.0
    
    for channel, percentage in allocations_dict.items():
        amount = (total_budget * percentage) / 100
        roi = CHANNEL_ROI.get(channel, 0)
        total_revenue += (amount * roi)
    
    projected_roi = total_revenue / total_budget if total_budget > 0 else 0
    return projected_roi, total_revenue

@router.post("/{movie_id}/budget-plan", response_model=BudgetPlanResponse)
async def create_or_update_budget_plan(
    movie_id: str,
    plan: BudgetPlanCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create or update budget plan for a movie
    """
    db = get_database()
    
    # Verify movie exists and user owns it
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Check if it's a historical movie
    if movie.get("tag") == "past":
        raise HTTPException(
            status_code=400,
            detail="Budget planning is only available for current movies"
        )
    
    # Calculate metrics
    allocations_dict = plan.allocations.dict()
    total_allocated = sum(allocations_dict.values())
    projected_roi, projected_revenue = calculate_projected_roi(plan.total_budget, plan.allocations)
    
    # Check if budget plan already exists
    existing_plan = await db.budget_plans.find_one({"movie_id": movie_id})
    
    budget_doc = {
        "movie_id": movie_id,
        "producer_id": str(current_user["_id"]),
        "total_budget": plan.total_budget,
        "allocations": allocations_dict,
        "timeline_weeks": plan.timeline_weeks,
        "total_allocated_percentage": total_allocated,
        "projected_roi": projected_roi,
        "projected_revenue": projected_revenue,
        "updated_at": datetime.utcnow()
    }
    
    if existing_plan:
        # Update existing plan
        await db.budget_plans.update_one(
            {"_id": existing_plan["_id"]},
            {"$set": budget_doc}
        )
        budget_id = str(existing_plan["_id"])
    else:
        # Create new plan
        budget_doc["created_at"] = datetime.utcnow()
        result = await db.budget_plans.insert_one(budget_doc)
        budget_id = str(result.inserted_id)
    
    return BudgetPlanResponse(
        id=budget_id,
        **budget_doc
    )

@router.get("/{movie_id}/budget-plan", response_model=Optional[BudgetPlanResponse])
async def get_budget_plan(
    movie_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get budget plan for a movie
    """
    db = get_database()
    
    # Verify movie exists and user owns it
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Get budget plan
    plan = await db.budget_plans.find_one({"movie_id": movie_id})
    
    if not plan:
        return None
    
    return BudgetPlanResponse(
        id=str(plan["_id"]),
        movie_id=plan["movie_id"],
        producer_id=plan["producer_id"],
        total_budget=plan["total_budget"],
        allocations=BudgetAllocations(**plan["allocations"]),
        timeline_weeks=plan["timeline_weeks"],
        total_allocated_percentage=plan["total_allocated_percentage"],
        projected_roi=plan["projected_roi"],
        projected_revenue=plan["projected_revenue"],
        created_at=plan["created_at"],
        updated_at=plan["updated_at"]
    )

@router.post("/{movie_id}/budget-plan/optimize")
async def optimize_budget(
    movie_id: str,
    request: BudgetOptimizationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Get AI-powered budget optimization recommendations using DeepSeek R1
    """
    db = get_database()
    
    # Verify movie exists and user owns it
    movie = await db.movies.find_one({"_id": ObjectId(movie_id)})
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if movie["producer_id"] != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Format currency
    def format_currency(amount):
        if amount >= 10000000:
            return f"₹{amount / 10000000:.2f}Cr"
        if amount >= 100000:
            return f"₹{amount / 100000:.2f}L"
        return f"₹{amount / 1000:.0f}K"
    
    # Build AI prompt for DeepSeek R1
    allocations_dict = request.current_allocations.dict()
    
    prompt = f"""You are a film marketing budget optimization expert specializing in Indian cinema. Analyze this budget allocation and provide tactical recommendations.

Film Details:
- Title: "{request.movie_title}"
- Genre: {request.genre}
- Production Budget: {format_currency(request.budget)}
- Marketing Budget: {format_currency(request.total_marketing_budget)}
- Campaign Timeline: {request.timeline_weeks} weeks before release

Current Channel Allocation:
- Digital Marketing: {allocations_dict['digital']}% ({format_currency(request.total_marketing_budget * allocations_dict['digital'] / 100)})
  Sub-channels: Social Media Ads, YouTube Pre-roll, Display Ads, Search Ads
  Average ROI: 3.2x
  
- Traditional Media: {allocations_dict['traditional']}% ({format_currency(request.total_marketing_budget * allocations_dict['traditional'] / 100)})
  Sub-channels: TV Spots, Print Ads, Radio, Outdoor
  Average ROI: 1.8x
  
- Influencer Marketing: {allocations_dict['influencer']}% ({format_currency(request.total_marketing_budget * allocations_dict['influencer'] / 100)})
  Sub-channels: Micro/Macro Influencers, Celebrity, Content Creators
  Average ROI: 2.5x
  
- Events & Activations: {allocations_dict['events']}% ({format_currency(request.total_marketing_budget * allocations_dict['events'] / 100)})
  Sub-channels: Premiere, Fan Meetups, College Tours, Mall Activations
  Average ROI: 2.0x
  
- PR & Media Relations: {allocations_dict['pr']}% ({format_currency(request.total_marketing_budget * allocations_dict['pr'] / 100)})
  Sub-channels: Press Releases, Interviews, Media Kit, Junkets
  Average ROI: 2.8x
  
- Contingency Reserve: {allocations_dict['contingency']}% ({format_currency(request.total_marketing_budget * allocations_dict['contingency'] / 100)})
  For emergency response and opportunity buys

Provide comprehensive recommendations in these sections:

1. BUDGET OPTIMIZATION
   - Which channels should be increased/decreased and by how much
   - Specific reasoning based on genre and ROI data
   - Optimal allocation percentages for this {request.genre} film

2. CHANNEL-SPECIFIC TACTICS
   - Detailed tactics for each major channel
   - Genre-specific strategies for {request.genre} movies
   - Platform-specific recommendations (Instagram, YouTube, etc.)

3. TIMELINE STRATEGY ({request.timeline_weeks} weeks)
   - Week-by-week spending breakdown
   - Key milestones and campaign phases
   - When to deploy each channel for maximum impact

4. RISK MITIGATION
   - Potential risks in current allocation
   - Contingency planning recommendations
   - How to handle underperforming channels

5. ROI IMPROVEMENTS
   - Expected ROI with optimized allocation
   - Specific metrics to track
   - Performance benchmarks for success

Format your response with clear headings and actionable bullet points."""

    try:
        # Use DeepSeek R1 via Ollama
        import requests
        
        ollama_url = f"{settings.OLLAMA_URL}/api/generate"
        
        try:
            print(f"Calling DeepSeek R1 for budget optimization...")
            response = requests.post(
                ollama_url,
                json={
                    "model": "deepseek-r1:7b",  # Use the full model name
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2000  # Limit response length for faster generation
                    }
                },
                timeout=180  # 3 minutes timeout for DeepSeek R1 (it's slow due to reasoning)
            )
            
            if response.status_code == 200:
                result = response.json().get('response', '')
                print(f"✓ DeepSeek R1 generated {len(result)} characters of recommendations")
                
                return {
                    "success": True,
                    "recommendations": result,
                    "source": "deepseek-r1:7b"
                }
            else:
                print(f"DeepSeek R1 error: {response.status_code}")
                raise Exception(f"DeepSeek R1 returned status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"DeepSeek R1 timeout (>180s) - falling back to rule-based")
            result = generate_fallback_recommendations(request)
            
            return {
                "success": True,
                "recommendations": result,
                "source": "fallback (timeout)"
            }
        except Exception as e:
            print(f"DeepSeek R1 failed: {e}")
            print("Falling back to rule-based recommendations...")
            result = generate_fallback_recommendations(request)
            
            return {
                "success": True,
                "recommendations": result,
                "source": "fallback"
            }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate optimization: {str(e)}"
        )

def generate_fallback_recommendations(request: BudgetOptimizationRequest) -> str:
    """Generate rule-based recommendations when AI is unavailable"""
    
    genre = request.genre.lower()
    allocations = request.current_allocations.dict()
    
    recommendations = f"""# Budget Optimization Recommendations for {request.movie_title}

## 1. Budget Optimization

"""
    
    # Genre-specific recommendations
    if genre in ["action", "thriller", "sci-fi"]:
        recommendations += """**For Action/Thriller/Sci-Fi:**
- Increase Digital Marketing to 35-40% (currently {:.0f}%) - These genres perform exceptionally well with YouTube pre-roll and social media ads
- Maintain Influencer at 20-25% - Gaming and tech influencers can drive significant buzz
- Consider reducing Traditional to 10-12% unless targeting older demographics
""".format(allocations['digital'])
    
    elif genre in ["drama", "romance"]:
        recommendations += """**For Drama/Romance:**
- Increase PR & Media Relations to 20-25% (currently {:.0f}%) - Critical reviews and word-of-mouth are crucial
- Boost Influencer to 25-30% - Lifestyle and entertainment influencers resonate well
- Digital can be 25-30% with focus on Instagram and Facebook
""".format(allocations['pr'])
    
    elif genre in ["comedy", "family"]:
        recommendations += """**For Comedy/Family:**
- Maximize Digital to 35-40% - Viral potential is high
- Increase Events to 15-20% (currently {:.0f}%) - Mall activations and family events work well
- Influencer at 20-25% with focus on family and comedy content creators
""".format(allocations['events'])
    
    else:
        recommendations += """**General Recommendations:**
- Digital Marketing: 30-35% - Core channel for all genres
- Influencer: 20-25% - Growing importance in Indian market
- Traditional: 12-18% - Still relevant for mass reach
"""
    
    recommendations += f"""
## 2. Channel-Specific Tactics

**Digital Marketing:**
- YouTube: Pre-roll ads on trending videos, trailer promotions
- Instagram: Reels, Stories, carousel posts with BTS content
- Facebook: Targeted ads to specific demographics
- Google Ads: Search campaigns for movie name and cast

**Influencer Marketing:**
- Micro-influencers (10K-100K): Better engagement rates, cost-effective
- Macro-influencers (100K-1M): Wider reach for key moments
- Celebrity collaborations: For trailer launch and premiere

**Events & Activations:**
- College tours: If targeting youth demographic
- Mall activations: Interactive experiences, photo booths
- Premiere events: Generate media coverage and social buzz

## 3. Timeline-Based Spending Strategy ({request.timeline_weeks} weeks)

**Weeks {request.timeline_weeks}-6: Awareness Phase (25% of budget)**
- Teaser campaigns on digital platforms
- PR seeding with entertainment journalists
- Initial influencer partnerships

**Weeks 5-3: Interest Phase (35% of budget)**
- Trailer launch with heavy digital push
- Influencer campaigns at peak
- Traditional media buys begin

**Weeks 2-1: Desire Phase (30% of budget)**
- Maximum digital spend
- Events and activations
- Final PR push

**Week 0: Action Phase (10% of budget)**
- Release day engagement
- Real-time social media
- Contingency for opportunities

## 4. Risk Mitigation

- Keep 10-15% contingency for crisis management or opportunity buys
- Diversify across channels to reduce dependency
- Monitor daily performance and be ready to reallocate
- Have backup plans for each major campaign element

## 5. Expected ROI Improvements

Current projected ROI: {request.total_marketing_budget * sum(CHANNEL_ROI.get(k, 0) * v / 100 for k, v in allocations.items()) / request.total_marketing_budget:.1f}x

With optimizations:
- Digital optimization: +15-20% efficiency
- Influencer targeting: +10-15% engagement
- Timeline optimization: +5-10% overall impact
- Expected improved ROI: {(request.total_marketing_budget * sum(CHANNEL_ROI.get(k, 0) * v / 100 for k, v in allocations.items()) / request.total_marketing_budget) * 1.2:.1f}x

**Key Success Metrics:**
- Track engagement rates daily
- Monitor ticket pre-bookings
- Measure social media sentiment
- Adjust spend based on performance
"""
    
    return recommendations
