# Fix Duplicate Producers Issue

## Problem
The seed script was creating NEW producer accounts instead of using EXISTING ones, causing:
- Duplicate producers with same name
- Movies not showing up for the original producers (like Dil Raju)
- Confusion about which producer account to use

## Root Cause
The script was filtering by `role: "producer"` field which doesn't exist in the User model. This caused the query to fail and no producers were found.

## Solution Applied

### 1. Fixed Producer Query
Removed the non-existent `role` filter and improved username matching:
```python
producer = await db.users.find_one({
    "$or": [
        {"full_name": producer_name},
        {"username": producer_name.lower().replace(" ", "")},
        {"username": producer_name.lower().replace(" ", "_")}
    ]
})
```

### 2. Added Debug Function
Added `list_all_users()` to show all users in database before processing.

### 3. Added Cleanup Function
Added `clean_duplicate_movies()` to remove movies created for wrong producer IDs.

### 4. Created Verification Script
Created `verify_producers.py` to check which producers exist in database.

## How to Fix Your Database

### Step 1: Verify Existing Producers
```bash
cd backend
python scripts/verify_producers.py
```

This will show:
- All users in your database
- Which expected producers are found/missing
- How many movies each producer has

### Step 2: Register Missing Producers (if any)
If any producers are missing, register them using the credentials from:
`backend/scripts/producer_credentials.txt`

Login URL: http://localhost:5173/register

Use these exact details:
- **Sukumar**: sukumar@filmproductions.com / sukumar / Producer@123
- **Dil Raju**: dilraju@filmproductions.com / dilraju / Producer@123
- **BVSN Prasad**: bvsnprasad@filmproductions.com / bvsnprasad / Producer@123
- **Prasad Devineni**: prasaddevineni@filmproductions.com / prasaddevineni / Producer@123
- **Samantha Ruth Prabhu**: samantharuthprabhu@filmproductions.com / samantharuthprabhu / Producer@123

### Step 3: Run Fixed Seed Script
```bash
cd backend
python scripts/seed_current_movies_existing.py
```

The script will now:
1. Show all users in database (debug)
2. Find existing producers by name/username
3. Clean up any duplicate movies from previous runs
4. Create 16 new movies for existing producers (3-4 each)
5. All movies release between Feb 23 - March 29, 2026

### Step 4: Verify Movies
Login as any producer and check "My Movies" section.

Example:
- Login as: dilraju@filmproductions.com / Producer@123
- Go to "My Movies"
- You should see 3-4 movies releasing in Feb-March 2026

## Expected Output

### Successful Run:
```
================================================================================
SEED MOVIES FOR EXISTING PRODUCERS
Release Window: February 23 - March 29, 2026
================================================================================

DEBUG: All Users in Database
================================================================================
Total users: 11

1. Sukumar
   Email: sukumar@filmproductions.com
   Username: sukumar
   ID: 507f1f77bcf86cd799439011

...

================================================================================
Finding Existing Producer Accounts
================================================================================
✓ Found: Sukumar
  Email: sukumar@filmproductions.com
  Username: sukumar
  ID: 507f1f77bcf86cd799439011

✓ Found: Dil Raju
  Email: dilraju@filmproductions.com
  Username: dilraju
  ID: 507f1f77bcf86cd799439012

...

================================================================================
Cleaning Duplicate Movies
================================================================================
Found 20 current movies in database

✓ VALID Producer: Sukumar (ID: 507f1f77bcf86cd799439011)
  Movies: 4

✗ INVALID (will delete) Producer: Sukumar (ID: 507f1f77bcf86cd799439999)
  Movies: 3
    ✗ Deleted: The Legend
    ✗ Deleted: Warrior
    ✗ Deleted: Rebel

✓ Cleaned up 3 duplicate/invalid movies

================================================================================
Creating Current Movie Projects
Release Window: Feb 23, 2026 - March 29, 2026
================================================================================

Sukumar - Creating 3 movies:
--------------------------------------------------------------------------------
  ✓ The Legend Returns
    Release: Feb 25, 2026
    Director: S. S. Rajamouli
    Cast: Allu Arjun & Sai Pallavi
    Budget: ₹25.0Cr | Status: awaiting-release

...

================================================================================
SUMMARY
================================================================================
✓ Existing producers found: 5
✓ Movies created: 16
✓ Release window: Feb 23 - March 29, 2026 (34 days)
✓ Info file: backend/scripts/existing_producers_info.txt

Producers with new movies:
  ✓ Sukumar
  ✓ Samantha Ruth Prabhu
  ✓ Dil Raju
  ✓ BVSN Prasad
  ✓ Prasad Devineni
```

## Troubleshooting

### Issue: "No existing producers found"
**Solution**: Register the producers first using the credentials file.

### Issue: "Movies not showing for Dil Raju"
**Solution**: 
1. Run `verify_producers.py` to check if there are duplicate Dil Raju accounts
2. The cleanup function will remove movies from wrong producer IDs
3. New movies will be created for the correct producer ID

### Issue: "Username mismatch"
**Solution**: The script tries multiple username formats:
- `dilraju` (no spaces)
- `dil_raju` (underscore)
- Full name: "Dil Raju"

Make sure your producer is registered with one of these formats.

## Files Modified
- `backend/scripts/seed_current_movies_existing.py` - Fixed producer query and added cleanup
- `backend/scripts/verify_producers.py` - New verification script
- `backend/scripts/FIX_DUPLICATE_PRODUCERS.md` - This guide

## Next Steps
1. Run verification script
2. Register any missing producers
3. Run seed script
4. Login and verify movies appear correctly
5. Use Release Strategy feature to see competitive environment
