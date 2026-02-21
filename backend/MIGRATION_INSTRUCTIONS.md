# 🚀 Historical Movies Migration - Ready to Run!

## Current Status
✅ Backend is running successfully on port 8000
✅ MongoDB is connected
✅ Migration scripts are ready
✅ All dependencies are installed

## What Will Happen

The migration script will:
1. Fetch all movies from `historical_movies` collection
2. Extract unique producer names
3. Create user accounts with:
   - Email: `producernamewithoutspa ces@gmail.com` (all lowercase, no spaces/special chars)
   - Password: `123456` (for all accounts)
   - Full name: Original producer name
4. Link all historical movies to their producer accounts via `producer_id`
5. Tag all historical movies as `"past"`
6. Generate `producer_credentials.txt` with all login details

## Run Migration Now

### Step 1: Open Terminal in Backend Folder
```bash
cd backend
```

### Step 2: Activate Virtual Environment (if not already active)
```bash
# Windows
venv\Scripts\activate

# You should see (venv) in your prompt
```

### Step 3: Run Migration Script
```bash
python scripts/migrate_historical_movies.py
```

### Step 4: Verify Migration
```bash
python scripts/verify_migration.py
```

## Expected Output

You should see something like:
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
  ... (more producers)

[3/5] Linking movies to producers...
✓ Linked 592 movies to producers

[4/5] Generating summary report...

[5/5] Migration Complete!
============================================================

PRODUCER ACCOUNTS CREATED:
------------------------------------------------------------
Producer Name                  Email                               Movies
------------------------------------------------------------
Sudhanskar Mikkil1neni        sudhanskarmi kkil1neni@gmail.com   15
Guntaka Srinivas Reddy        guntakasrinivasreddy@gmail.com     8
...

✓ Credentials saved to: producer_credentials.txt
```

## After Migration

### 1. Check Credentials File
```bash
cat scripts/producer_credentials.txt
# or open it in your editor
```

### 2. Test Login
1. Go to http://localhost:5174/login
2. Use any email from the credentials file
3. Password: `123456`
4. You should see their historical movies!

### 3. Verify in MongoDB
You can check in MongoDB Compass:
- Collection: `users` - should have new producer accounts with `is_migrated: true`
- Collection: `historical_movies` - should have `producer_id` and `tag: "past"`

## Troubleshooting

### If MongoDB is not running:
```bash
# Start MongoDB service
# Windows: Check Services app or run:
net start MongoDB
```

### If you get import errors:
```bash
# Make sure you're in the backend folder with venv activated
pip install -r requirements.txt
```

### If migration fails midway:
The script is idempotent - you can run it again safely. It will:
- Skip existing users
- Update movies that weren't linked yet

## Rollback (if needed)

If something goes wrong, you can rollback:

```javascript
// In MongoDB Compass or mongo shell
use film_intel_db

// Remove migrated users
db.users.deleteMany({ is_migrated: true })

// Remove producer_id from historical movies
db.historical_movies.updateMany(
  {},
  { $unset: { producer_id: "", tag: "" } }
)
```

## Next Steps After Migration

1. ✅ Test login with migrated producer accounts
2. ✅ Verify historical movies show up in their dashboard
3. ✅ Create new "current" movies for testing
4. ✅ Test competitor analysis with release dates
5. ✅ Test PR strategy generation

## Files Created

- `scripts/producer_credentials.txt` - All login credentials
- Migration logs in terminal output

## Safety Features

- ✅ Idempotent - safe to run multiple times
- ✅ Skips existing users automatically
- ✅ Preserves existing data
- ✅ Adds `is_migrated: true` flag for easy identification
- ✅ No data deletion, only additions and updates

---

**Ready to migrate? Run the command above! 🎬**
