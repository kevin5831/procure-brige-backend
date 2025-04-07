from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.auth import create_access_token, verify_token
from app.models.user import User
from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    sub: str

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(data: LoginRequest):
    # print(f"email {data.email} and password {data.password} ")
    user = await User.filter(email=data.email).first()
    if not user or not pwd_context.verify(data.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"email": user.email, "first_name":user.first_name ,"last_name": user.last_name })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register")
async def register(data: RegisterRequest):
    existing_user = await User.filter(email=data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(data.password)
    user = await User.create(
        email=data.email,
        password=hashed_password,
        first_name=data.first_name,
        last_name = data.last_name
    )
    
    token = create_access_token({"email": user.email, "first_name":user.first_name ,"last_name": user.last_name })
    return {"access_token": token, "token_type": "bearer"}

@router.post("/me")
async def get_current_user(payload: dict = Depends(verify_token)):
    return payload
