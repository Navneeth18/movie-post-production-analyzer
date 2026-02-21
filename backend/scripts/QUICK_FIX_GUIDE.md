# Quick Fix Guide - Duplicate Producers Issue

## The Problem
Dil Raju's movies (and other producers) are not showing up because the seed script created DUPLICATE producer accounts instead of using existing ones.

## The Fix (3 Simple Steps)

### Step 1: Check Which Producers Exist
```bash
cd backend
python scripts/verify_producers.py
```

This shows all users and which producers are found/missing.

### Step 2: Register Missing Producers (if needed)
If any producers are missing, register them at: http://localhost:5173/register

Use credentials from: `backend/scripts/producer_credentials.txt`

**Key Producers to Register:**
- Sukumar: sukumar@filmproductions.com / sukumar / Producer@123
- Dil Raju: dilraju@filmproductions.com / dilraju / Producer@123  
- BVSN Prasad: bvsnprasad@filmproductions.com / bvsnprasad / Producer@123
- Prasad Devineni: prasaddevineni@filmproductions.com / prasaddevineni / Producer@123
- Sahu Garapati: sahugarapati@filmproductions.com / sahugarapati / Producer@123

### Step 3: Run Fixed Seed Script
```bash
cd backend
python scripts/seed_current_movies_existing.py
```

This will:
- ✓ Find existing producers (no duplicates)
- ✓ Clean up wrong movies from previous runs
- ✓ Create 16 new movies for 5 producers
- ✓ All movies release Feb 23 - March 29, 2026

## Verify It Worked

Login as Dil Raju:
- Email: dilraju@filmproductions.com
- Password: Producer@123
- Go to "My Movies"
- You should see 3-4 movies releasing in Feb-March 2026

## What Was Fixed

### Before (BROKEN):
```python
# This query failed because 'role' field doesn't exist
producer = await db.users.find_one({
    "full_name": "Dil Raju",
    "role": "producer"  # ❌ This field doesn't exist!
})
# Result: None (not found)
# Script creates NEW producer → Duplicate!
```

### After (FIXED):
```python
# This query works - no role filter
producer = await db.users.find_one({
    "$or": [
        {"full_name": "Dil Raju"},
        {"username": "dilraju"},
        {"username": "dil_raju"}
    ]
})
# Result: Found existing producer ✓
# Script uses existing producer → No duplicates!
```

## Files Changed
- `seed_current_movies_existing.py` - Fixed query, added cleanup
- `verify_producers.py` - New verification tool
- `FIX_DUPLICATE_PRODUCERS.md` - Detailed guide
- `QUICK_FIX_GUIDE.md` - This file

## Credentials File Location
`backend/scripts/producer_credentials.txt`

This file contains all producer login details with the correct email format (no dots).
