from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class AssetSchema(BaseModel):
    id: int
    asset_id: str
    company: int
    name: str
    category: str
    location: Optional[int]
    purchase_price: float
    purchase_date: date
    status: str

    class Config:
        from_attributes = True

class VendorSchema(BaseModel):
    id: int
    vendor_id: str
    company: int
    name: str
    email: EmailStr
    phone: str
    address: Optional[str]
    service_categories: str
    status: str

    class Config:
        from_attributes = True

class MaintenanceSchema(BaseModel):
    id: int
    task_id: str
    asset: int
    company: int
    maintenance_type: str
    description: str
    scheduled_date: date
    cost: float
    vendor: Optional[int]
    status: str

    class Config:
        from_attributes = True
