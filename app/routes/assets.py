from fastapi import APIRouter, Depends, HTTPException
from app.models.assets import Asset, Maintenance, Vendor
from app.schemas.assets import AssetSchema, MaintenanceSchema, VendorSchema
from app.utils import success_response, error_response

router = APIRouter()

# ✅ List & Create Assets
@router.get("/", response_model=list[AssetSchema])
async def list_assets():
    return await Asset.all()

@router.post("/", response_model=AssetSchema)
async def create_asset(asset_data: AssetSchema):
    asset = await Asset.create(**asset_data.dict())
    return asset

# ✅ Retrieve Asset by ID
@router.get("/{asset_id}", response_model=AssetSchema)
async def get_asset(asset_id: str):
    asset = await Asset.get_or_none(asset_id=asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

# ✅ List & Create Vendors
@router.get("/vendors", response_model=list[VendorSchema])
async def list_vendors():
    return await Vendor.all()

@router.post("/vendors", response_model=VendorSchema)
async def create_vendor(vendor_data: VendorSchema):
    vendor = await Vendor.create(**vendor_data.dict())
    return vendor

# ✅ List & Create Maintenance Records
@router.get("/maintenance", response_model=list[MaintenanceSchema])
async def list_maintenance():
    return await Maintenance.all()

@router.post("/maintenance", response_model=MaintenanceSchema)
async def create_maintenance(maintenance_data: MaintenanceSchema):
    maintenance = await Maintenance.create(**maintenance_data.dict())
    return maintenance
