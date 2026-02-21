# ⚡ Quick Migration Guide

## TL;DR - Run These Commands

```bash
# 1. Navigate to backend folder
cd backend

# 2. Activate virtual environment (if not active)
venv\Scripts\activate

# 3. Run migration
python scripts/migrate_historical_movies.py

# 4. Verify migration
python scripts/verify_migration.py

# 5. Check credentials
cat scripts/producer_credentials.txt
```

## What Happens

✅ Creates user accounts for all producers in historical_movies
✅ Email format: `producername@gmail.com` (no spaces, lowercase)
✅ Password: `123456` for all accounts
✅ Links historical movies to producers via `producer_id`
✅ Tags all historical movies as `"past"`
✅ Generates `producer_credentials.txt` file

## Test Login

1. Open http://localhost:5174/login
2. Use email from `producer_credentials.txt`
3. Password: `123456`
4. See historical movies in dashboard

## Files Generated

- `scripts/producer_credentials.txt` - All login credentials

## Safe to Run Multiple Times

The script is idempotent:
- Skips existing users
- Only updates movies that need linking
- No data loss

## Need Help?

See `MIGRATION_INSTRUCTIONS.md` for detailed guide.
