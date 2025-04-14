from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict, Any
from datetime import date

class AssetSchema(BaseModel):
    id: Optional[int] = None
    asset_id: Optional[str] = Field(None, description="Auto created and Unique identifier for the asset (e.g., AST-1234)")
    company: int = Field(..., description="ID of the company that owns the asset")
    location: int = Field(..., description="company location (e.g. 2)")
    name: str = Field(..., description="asset name (e.g. Dell 18 Laptop)")
    category: str = Field(..., description="asset category (e.g. Furniture,	IT Equipment, Furniture, Vehicle)")
    department: str = Field(..., description="department for asset (e.g IT Department, Finance, Human Resources	)")
    assigned: str = Field(..., description="assigned to User (e.g Jone Doe, Kevin)")
    asset_details: Optional[Dict[str, Any]] = Field(..., description="object to show asset in detial")
    purchase_price: float = Field(..., description="asset purchase_price (e.g 1200)")
    purchase_date: date = Field(..., description="date when asset purchased (e.g 2025-03-12)")
    status: Optional[str] = Field(None, description="asset status (e.g in service, pending, disposed)")
    
    class Config:
        from_attributes = True

class VendorSchema(BaseModel):
    vendor_id: Optional[str] = Field(None, description="Auto created and Unique identifier for the vendor (e.g., VEN-001)")
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
    task_id: Optional[str] = Field(None, description="Auto created and Unique identifier for the maintenance (e.g., MAINT-001)")
    asset: int
    company: int
    maintenance_type: str
    description: str
    scheduled_date: date
    cost: float
    vendor: Optional[int] = None
    status: str

    class Config:
        from_attributes = True


class AssetTransferSchema(BaseModel):
    asset: int
    company: Optional[int] = None
    from_location: Optional[int] = None
    from_department: Optional[str] = None
    from_assigned: Optional[str] = None
    to_location: int
    to_department: str
    to_assigned: str
    transferred_by: str
    transfer_date: date
    status: str = "pending"
    note: Optional[str] = None

    class Config:
        from_attributes = True


class AssetDisposalSchema(BaseModel):
    asset: int
    company: Optional[int] = None
    method: str  # sale, scrap, donation
    disposal_date: date
    value_received: float
    note: Optional[str]
    approved_by: str

    class Config:
        from_attributes = True
