# Starting the Backend

## Prerequisites

1. **MongoDB must be running**
   - Windows: Start MongoDB service or run `mongod`
   - Mac: `brew services start mongodb-community`
   - Linux: `sudo systemctl start mongod`

2. **Python dependencies installed**
   ```bash
   pip install -r requirements.txt
   ```

## Start the Backend

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Test the Backend

1. **Check if backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Test registration (optional):**
   ```bash
   python test_registration.py
   ```

## Common Issues

### Issue: "Database connection not available"
**Solution:** Make sure MongoDB is running
```bash
# Check if MongoDB is running
# Windows
sc query MongoDB

# Mac/Linux
ps aux | grep mongod
```

### Issue: "Module not found"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution:** Kill the process or use a different port
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

## Verify Registration Works

1. Start the backend
2. Go to http://localhost:8000/docs
3. Try the `/api/v1/auth/register` endpoint
4. Use this test data:
   ```json
   {
     "email": "producer@test.com",
     "username": "producer1",
     "password": "test123",
     "full_name": "Test Producer"
   }
   ```

## Backend URLs

- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
