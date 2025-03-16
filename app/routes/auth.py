from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from app.auth import create_access_token, verify_token
from app.models.user import User

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def login(email: str, password: str):
    user = await User.filter(email=email).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
async def get_current_user(token: str = Depends(verify_token)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token
