# Historical Movies Migration Guide

## What This Does

This script will:
1. ✅ Find all unique producers in `historical_movies` collection
2. ✅ Create user accounts for each producer
3. ✅ Generate emails as `producername@gmail.com` (no spaces)
4. ✅ Set default password as `123456` for all accounts
5. ✅ Link all historical movies to their producer accounts
6. ✅ Tag all historical movies as "past"
7. ✅ Generate a credentials file with all login details

## Prerequisites

1. **MongoDB must be running**
2. **Backend dependencies installed**

## Run Migration

```bash
cd backend
python scripts/migrate_historical_movies.py
```

## Expected Output

```
============================================================
HISTORICAL MOVIES MIGRATION SCRIPT
============================================================

[1/5] Fetching historical movies...
✓ Found 592 historical movies
✓ Found 45 unique producers

[2/5] Creating producer accounts...
  ✓ Created: Sudhanskar Mikkil1neni → sudhanskarmi kkil1neni@gmail.com
  ✓ Created: Guntaka Srinivas Reddy → guntakasrinivasreddy@gmail.com
  ...

[3/5] Linking movies to producers...
✓ Linked 592 movies to producers

[4/5] Generating summary report...

[5/5] Migration Complete!
```

## Verify Migration

```bash
python scripts/verify_migration.py
```

## Output Files

- `producer_credentials.txt` - Contains all producer login credentials

## Sample Credentials

```
Producer Name                  Email                               Password
--------------------------------------------------------------------------------
Sudhanskar Mikkil1neni        sudhanskarmi kkil1neni@gmail.com   123456
Guntaka Srinivas Reddy        guntakasrinivasreddy@gmail.com     123456
```

## Test Login

1. Go to http://localhost:5174/login
2. Use any email from `producer_credentials.txt`
3. Password: `123456`
4. You should see their historical movies in the dashboard

## Rollback (if needed)

```javascript
// In MongoDB Compass or shell
use film_intel_db

// Remove migrated users
db.users.deleteMany({ is_migrated: true })

// Remove producer_id from historical movies
db.historical_movies.updateMany(
  {},
  { $unset: { producer_id: "", tag: "", status: "" } }
)
```

## Notes

- Script is idempotent - safe to run multiple times
- Existing users won't be duplicated
- Movies without producer info will be skipped
- All accounts are marked with `is_migrated: true` flag
