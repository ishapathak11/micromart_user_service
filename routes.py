from fastapi import APIRouter, HTTPException
from models import UserCreate, UserLogin, User, UserResponse
from utils import hash_password, verify_password, create_jwt_token
from db import db

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed = hash_password(user_data.password)
    user = User(email=user_data.email, first_name=user_data.first_name, last_name=user_data.last_name)
    user_dict = user.dict()
    user_dict["password"] = hashed
    await db.users.insert_one(user_dict)
    token = create_jwt_token(user.id)
    return UserResponse(user=user, token=token)

@router.post("/login", response_model=UserResponse)
async def login_user(login_data: UserLogin):
    user_data = await db.users.find_one({"email": login_data.email})
    if not user_data or not verify_password(login_data.password, user_data["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    user = User(**user_data)
    token = create_jwt_token(user.id)
    return UserResponse(user=user, token=token)
