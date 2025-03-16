from pydantic import BaseModel, EmailStr
from typing import Optional

class CompanySchema(BaseModel):
    id: int
    name: str
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    website: Optional[str]
    address: Optional[str]

    class Config:
        from_attributes = True

class LocationSchema(BaseModel):
    id: int
    company: int
    name: str
    code: str
    location_type: str
    country: str
    city: str
    address: str

    class Config:
        from_attributes = True

class DepartmentSchema(BaseModel):
    id: int
    company: int
    name: str
    description: str
    manager: Optional[int]

    class Config:
        from_attributes = True

class InvitationSchema(BaseModel):
    id: int
    invitation_id: str
    company: int
    name: str
    email: EmailStr
    role: str
    department: Optional[int]
    status: str

    class Config:
        from_attributes = True
