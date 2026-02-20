# Troubleshooting Guide

## Registration Not Working

### Step 1: Check if MongoDB is Running

**Windows:**
```bash
sc query MongoDB
# or
net start MongoDB
```

**Mac:**
```bash
brew services list | grep mongodb
# or start it
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl status mongod
# or start it
sudo systemctl start mongod
```

### Step 2: Check if Backend is Running

1. Open http://localhost:8000/health in your browser
2. You should see: `{"status":"healthy","database":"connected"}`

If not, start the backend:
```bash
cd backend
uvicorn app.main:app --reload
```

### Step 3: Test Registration via Swagger

1. Go to http://localhost:8000/docs
2. Find `/api/v1/auth/register` endpoint
3. Click "Try it out"
4. Use this test data:
```json
{
  "email": "test@example.com",
  "username": "testuser",
  "password": "test123",
  "full_name": "Test User"
}
```
5. Click "Execute"

### Step 4: Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Try to register
4. Look for error messages

Common errors:
- **Network Error**: Backend not running
- **CORS Error**: Backend CORS not configured
- **500 Error**: Database connection issue

### Step 5: Run Test Script

```bash
cd backend
python test_registration.py
```

This will test:
- MongoDB connection
- Password hashing
- User creation

## Common Issues

### Issue: "Database connection not available"

**Cause:** MongoDB is not running

**Solution:**
```bash
# Windows
net start MongoDB

# Mac
brew services start mongodb-community

# Linux
sudo systemctl start mongod
```

### Issue: "CORS Error" in Browser

**Cause:** Frontend URL not in CORS whitelist

**Solution:** Check `backend/app/main.py` has your frontend URL:
```python
allow_origins=["http://localhost:5174", "http://localhost:5173"]
```

### Issue: "Module 'passlib' not found"

**Cause:** Missing dependencies

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"

**Cause:** Another process using port 8000

**Solution:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### Issue: Frontend shows "Network Error"

**Cause:** Backend not running or wrong URL

**Solution:**
1. Check backend is running: http://localhost:8000/health
2. Check `.env` in frontend_new:
```
VITE_API_URL=http://localhost:8000
```
3. Restart frontend:
```bash
cd frontend_new
npm run dev
```

## Testing the Full Flow

1. **Start MongoDB**
2. **Start Backend:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
3. **Start Frontend:**
   ```bash
   cd frontend_new
   npm run dev
   ```
4. **Test Registration:**
   - Go to http://localhost:5174/register
   - Fill in the form
   - Click Register
   - Should redirect to login

5. **Test Login:**
   - Use the credentials you just created
   - Should redirect to dashboard

## Still Not Working?

Check the backend logs for detailed error messages:
```bash
cd backend
uvicorn app.main:app --reload --log-level debug
```

Check browser console (F12) for frontend errors.

## Quick Test Commands

```bash
# Test MongoDB
mongo --eval "db.version()"

# Test Backend
curl http://localhost:8000/health

# Test Registration
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"test123","full_name":"Test"}'
```
