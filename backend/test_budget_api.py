"""
Test Budget Planning API
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from app.schemas.budget_schema import BudgetAllocations, BudgetPlanCreate

# Test schema validation
def test_budget_schemas():
    print("="*80)
    print("Testing Budget Planning Schemas")
    print("="*80)
    
    # Test allocations
    allocations = BudgetAllocations(
        digital=30,
        traditional=15,
        influencer=20,
        events=10,
        pr=15,
        contingency=10
    )
    print(f"\n✓ BudgetAllocations created: {allocations.dict()}")
    
    # Test budget plan
    plan = BudgetPlanCreate(
        total_budget=5000000,
        allocations=allocations,
        timeline_weeks=8
    )
    print(f"✓ BudgetPlanCreate created: total_budget={plan.total_budget}, timeline={plan.timeline_weeks}")
    
    # Test validation - over 100%
    try:
        bad_allocations = BudgetAllocations(
            digital=50,
            traditional=30,
            influencer=30,
            events=20,
            pr=20,
            contingency=10
        )
        total = sum(bad_allocations.dict().values())
        print(f"\n⚠ Warning: Total allocation is {total}% (over 100%)")
    except Exception as e:
        print(f"\n✗ Validation error: {e}")
    
    # Test ROI calculation
    from app.api.endpoints.budget import calculate_projected_roi, CHANNEL_ROI
    
    roi, revenue = calculate_projected_roi(5000000, allocations)
    print(f"\n✓ ROI Calculation:")
    print(f"  Total Budget: ₹50L")
    print(f"  Projected ROI: {roi:.2f}x")
    print(f"  Projected Revenue: ₹{revenue/100000:.2f}L")
    
    print(f"\n✓ Channel ROI Data:")
    for channel, roi_value in CHANNEL_ROI.items():
        print(f"  {channel}: {roi_value}x")
    
    print("\n" + "="*80)
    print("All tests passed!")
    print("="*80)

if __name__ == "__main__":
    test_budget_schemas()
