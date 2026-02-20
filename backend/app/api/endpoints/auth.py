from fastapi import APIRouter, HTTPException, status, Depends
from datetime import timedelta, datetime
from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserResponse
from app.services.auth_service import get_password_hash, verify_password, create_access_token
from app.db.mongodb import get_database
from app.core.config import settings
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister):
    try:
        db = get_database()
        
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
        
        # Check if user exists
        existing_user = await db.users.find_one({"email": user_data.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check username
        existing_username = await db.users.find_one({"username": user_data.username})
        if existing_username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        
        # Create user
        user_dict = {
            "email": user_data.email,
            "username": user_data.username,
            "full_name": user_data.full_name,
            "hashed_password": get_password_hash(user_data.password),
            "is_active": True,
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_dict)
        user_dict["id"] = str(result.inserted_id)
        
        return UserResponse(
            id=user_dict["id"],
            email=user_dict["email"],
            username=user_dict["username"],
            full_name=user_dict.get("full_name"),
            is_active=user_dict["is_active"]
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    try:
        db = get_database()
        
        if db is None:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database connection not available"
            )
        
        user = await db.users.find_one({"email": user_data.email})
        if not user or not verify_password(user_data.password, user["hashed_password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user["email"]}, expires_delta=access_token_expires
        )
        
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=str(current_user["_id"]),
        email=current_user["email"],
        username=current_user["username"],
        full_name=current_user.get("full_name"),
        is_active=current_user["is_active"]
    )
