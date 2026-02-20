# Quick Start Guide

## The Issue

The error `ERR_CONNECTION_REFUSED` means **the backend is NOT running**.

## Fix Steps

### 1. Install Dependencies (Simplified)

```bash
cd backend
pip install fastapi uvicorn motor pymongo python-dotenv pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart bcrypt httpx
```

### 2. Start MongoDB

**Windows:**
```bash
net start MongoDB
```

**Mac:**
```bash
brew services start mongodb-community
```

**Linux:**
```bash
sudo systemctl start mongod
```

### 3. Start Backend

```bash
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
✓ MongoDB connected
```

### 4. Test Backend

Open in browser: http://localhost:8000/health

Should show:
```json
{"status":"healthy","database":"connected"}
```

### 5. Start Frontend

```bash
cd frontend_new
npm run dev
```

### 6. Test Registration

Go to: http://localhost:5174/register

Fill in:
- Full Name: Test User
- Username: testuser
- Email: test@example.com
- Password: test123

Click Register → Should redirect to login

## Common Issues

### "Module not found"
```bash
pip install <module-name>
```

### "Port 8000 in use"
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

### "MongoDB not running"
Check if MongoDB service is started (see step 2)

## Verify Everything Works

1. Backend health: http://localhost:8000/health
2. API docs: http://localhost:8000/docs
3. Frontend: http://localhost:5174

## Still Not Working?

Run this diagnostic:
```bash
cd backend
python -c "import fastapi, uvicorn, motor; print('✓ All core modules installed')"
```

If it fails, install missing modules individually.
