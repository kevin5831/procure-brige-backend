from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

class PermissionSchema(BaseModel):
    name: str
    codename: str

class UserSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    user_type: str
    role: Optional[str]
    is_staff: bool
    is_active: bool
    company: Optional[int]  # Company ID
    department: Optional[int]  # Department ID
    permissions: List[int]

    class Config:
        from_attributes = True  # Equivalent to Django's `orm_mode`
