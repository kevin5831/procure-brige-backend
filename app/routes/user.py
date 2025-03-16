from fastapi import APIRouter, Depends, HTTPException
from app.models.user import User, Permission
from app.schemas.user import UserSchema, PermissionSchema
from app.database import init_db

router = APIRouter()

@router.get("/", response_model=list[UserSchema])
async def list_users():
    return await User.all()

@router.post("/", response_model=UserSchema)
async def create_user(user_data: UserSchema):
    user = await User.create(**user_data.dict())
    return user

@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/permissions", response_model=list[PermissionSchema])
async def list_permissions():
    return await Permission.all()
