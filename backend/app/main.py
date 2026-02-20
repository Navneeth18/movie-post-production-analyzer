from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.db.mongodb import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Film Intel Backend", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()
    print("✓ MongoDB connected")

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()
    print("✓ MongoDB disconnected")

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Film Intel API", "version": "1.0.0", "status": "running"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}
