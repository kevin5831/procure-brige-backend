from fastapi import APIRouter, Depends, HTTPException
from app.models.assets import Asset, AssetTransfer, AssetDisposal, Maintenance, Vendor
from app.schemas.assets import AssetSchema, AssetTransferSchema, AssetDisposalSchema, MaintenanceSchema, VendorSchema
from app.models.company import Company, Location
router = APIRouter()

# ✅ List & Create Assets
@router.get("/", response_model=list[AssetSchema])
async def list_assets():
    """
    Get All Assets List

    URL : http://16.171.11.180/api/assets/

    """ 
    assets = await Asset.all()

    result = []
    for asset in assets:
        result.append({
            "id": asset.id,
            "asset_id": asset.asset_id,
            "company": asset.company_id, 
            "location": asset.location_id,  
            "name": asset.name,
            "category": asset.category,
            "department": asset.department,
            "assigned": asset.assigned,
            "purchase_price": asset.purchase_price,
            "purchase_date": asset.purchase_date,
            "status": asset.status
        })
    
    return result

@router.post("/", response_model=AssetSchema)
async def create_asset(asset_data: AssetSchema):
    """
    Create a new asset request Sample.

    Request Body:

    {

        "company": 1,

        "name": "Dell 18 Laptop",

        "category": "it_equipment",

        "location": 1,

        "department": "Finance",

        "assigned": "Jone Doe",

        "purchase_price": 1200.00,

        "purchase_date": "2025-04-15"

        "asset_details": {

            "it_category": "Laptop",

            "brand_model": "HP EliteBook G8",

            "processor": "Intel i7-1165G7",

            "memory": "16GB DDR4",

            "storage": "512GB SSD",

            "color": "Silver",

            "condition_grade": "B",

            "condition_notes": "Minor wear on keyboard",

            "other_specification": "Windows 11 Pro, 14-inch FHD Display"

        }

    }

    URL: http://16.171.11.180/api/assets/
    """ 
    # Get the related Company instance
    company = await Company.get(id=asset_data.company)
    location = await Location.get(id=asset_data.location)
    asset = await Asset.create(
        company=company,
        name=asset_data.name,
        location=location,
        category=asset_data.category,
        department = asset_data.department,
        assigned= asset_data.assigned,
        purchase_price=asset_data.purchase_price,
        purchase_date=asset_data.purchase_date,
        asset_details=asset_data.asset_details
    )
    
    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "company": asset.company.id,
        "location": asset.location.id,
        "name": asset.name,
        "category": asset.category,
        "department": asset.department,
        "assigned": asset.assigned,
        "purchase_price": asset.purchase_price,
        "purchase_date": asset.purchase_date,
        "status": asset.status,
        "asset_details": asset.asset_details
    }

# ✅ Create Transfer
@router.post("/transfer", response_model=AssetTransferSchema)
async def transfer_asset(data: AssetTransferSchema):
    """
    Create transfer asset

    Request Body

    {
    "asset":  3,
    "to_department": "Finance",
    "to_assigned": "Jone Doe",
    "to_location": 3,
    "transferred_by": "Kevin",
    "transfer_date": "2025-04-16",
    "note": "this is sample transfer"
    }

    URL: http://16.171.11.180/api/assets/transfer

    """ 
    asset = await Asset.get(id=data.asset)
    
    if asset.status == "Disposed":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot transfer of this asset",
                "reason": "Asset is already disposed"
            }
        )
    
    from_location_id = asset.location_id
    from_department = asset.department
    from_assigned = asset.assigned
    
    company_id = asset.company_id
    company = None
    if company_id:
        company = await Company.get(id=company_id)

    from_location = None
    if from_location_id:
        from_location = await Location.get(id=from_location_id)
    
    to_location = await Location.get(id=data.to_location)

    asset.location = to_location
    asset.assigned = data.to_assigned
    asset.department = data.to_department
    asset.status = "pending"
    
    await asset.save()
    
    transfer = await AssetTransfer.create(
        asset=asset,
        company=company,
        from_location=from_location,
        from_department=from_department,
        from_assigned=from_assigned,
        to_location=to_location,
        to_department=data.to_department,
        to_assigned=data.to_assigned,
        transferred_by=data.transferred_by,
        transfer_date=data.transfer_date,
        note=data.note or ""
    )
    
    return {
        "asset": asset.id,
        "company":company_id,
        "from_location": from_location_id,  
        "from_department": from_department,
        "from_assigned": from_assigned,
        "to_location": to_location.id,  
        "to_department": data.to_department,
        "to_assigned": data.to_assigned,
        "transferred_by": data.transferred_by,
        "transfer_date": data.transfer_date,
        "note": data.note or ""
    }

# ✅ Create Dispost
@router.post("/disposal", response_model=dict)
async def dispose_asset(data: AssetDisposalSchema):
    """
    Asset Diposal

    Request Body:

    {
        "asset":2,
        "method":"denote",
        "disposal_date":"2025-04-12",
        "value_received": 1200,
        "note":"simple note",
        "approved_by":"data"
    }

    URL : http://16.171.11.180/api/assets/disposal
    
    """
    asset = await Asset.get(id=data.asset)

    if asset.status == "Disposed":
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Cannot dispose of this asset",
                "reason": "Asset is already disposed"
            }
        )
    
    company_id = asset.company_id
    company = None
    if company_id:
        company = await Company.get(id=company_id)

    await AssetDisposal.create(
        asset=asset,
        company=company,
        method=data.method,
        disposal_date=data.disposal_date,
        value_received=data.value_received,
        note=data.note,
        approved_by=data.approved_by
    )

    asset.status = "Disposed"
    await asset.save()

    return {
        "asset": asset.id,
        "status": asset.status,
        "message": "Asset disposed successfully"
    }

# ✅ List & Create Vendors
@router.get("/{company_id}/vendors", response_model=list[VendorSchema])
async def list_vendors(company_id: int):
    """
    Get All Vendors List

    URL : http://16.171.11.180/api/assets/1/vendors

    """ 
    
    vendors = await Vendor.filter(company_id=company_id)
    if not vendors:
        raise HTTPException(status_code=404, detail="No vendors found")
        
    result = []
    for vendor in vendors:
        result.append({
            "vendor_id": vendor.vendor_id,
            "company": vendor.company_id, 
            "name": vendor.name,
            "email": vendor.email,
            "phone": vendor.phone,
            "address": vendor.address,
            "service_categories": vendor.service_categories,
            "status": vendor.status
        })
    
    return result

@router.post("/vendors", response_model=VendorSchema)
async def create_vendor(vendor_data: VendorSchema):
    """
    Create a new asset request Sample.

    Request Body:

    {

        "company": 1,

        "name": "Dell 18 Laptop",

        "email": "kookyzhang99@gmail.com",
        
        "phone" : "380 63 596 0361",
        
        "address": "address_1",
        
        "service_categories": "HVAC, Electronics",
        
        "status": "active"

    }

    URL: http://16.171.11.180/api/assets/vendors
    """ 

    company = await Company.get(id=vendor_data.company)
    vendor = await Vendor.create(
        company= company,
        name= vendor_data.name,
        email= vendor_data.email,
        phone= vendor_data.phone,
        address= vendor_data.address,
        service_categories= vendor_data.service_categories,
        status= vendor_data.status
    )
    return {
        "vendor_id": vendor.vendor_id,
        "company": company.id,
        "name": vendor.name,
        "email": vendor.email,
        "phone" : vendor.phone,
        "address": vendor.address,
        "service_categories": vendor.service_categories,
        "status": vendor.status
    }

# ✅ List & Create Maintenance Records
@router.get("/{company_id}/maintenance", response_model=list[MaintenanceSchema])
async def list_maintenance(company_id: int):
    """
    Get All Maintenance List

    URL : http://16.171.11.180/api/assets/2/maintenance

    """ 
    Maintenances = await Maintenance.filter(company_id=company_id)
    if not Maintenances:
        raise HTTPException(status_code=404, detail="No Maintenance found")
        
    result = []
    for maintenance in Maintenances:
        result.append({
            "task_id": maintenance.task_id,
            "asset": maintenance.asset_id,
            "company": maintenance.company_id,
            "maintenance_type": maintenance.maintenance_type,
            "description": maintenance.description,
            "scheduled_date": maintenance.scheduled_date,
            "cost": maintenance.cost,
            "vendor": getattr(maintenance.vendor, 'id', None),
            "status": maintenance.status
        })
    
    return result

@router.post("/maintenance", response_model=MaintenanceSchema)
async def create_maintenance(maintenance_data: MaintenanceSchema):
    """
    Create a new asset request Sample.

    For external maintenance (requiring a vendor):

    {

        "asset": 1,

        "company": 2,

        "maintenance_type": "external",

        "description": "description",

        "scheduled_date": "2025-05-12",

        "cost": 2000,

        "vendor": 1,

        "status": "scheduled"

    }

    For internal maintenance (no vendor required):

    {

        "asset": 1,

        "company": 2,

        "maintenance_type": "internal",

        "description": "description",

        "scheduled_date": "2025-05-12",

        "cost": 2000,

        "status": "scheduled"

    }

    URL: http://16.171.11.180/api/assets/maintenance
    """ 

    asset = await Asset.get(id=maintenance_data.asset)
    company = await Company.get(id=maintenance_data.company)
    
    vendor = None
    if maintenance_data.vendor is not None:
        vendor = await Vendor.get(id=maintenance_data.vendor)
    
    maintenance = await Maintenance.create(
        asset= asset,
        company= company,
        maintenance_type= maintenance_data.maintenance_type,
        description= maintenance_data.description,
        scheduled_date= maintenance_data.scheduled_date,
        cost= maintenance_data.cost,
        vendor= vendor,
        status= maintenance_data.status
    )
    return {
        "task_id": maintenance.task_id,
        "asset": asset.id,
        "company": company.id,
        "maintenance_type": maintenance.maintenance_type,
        "description": maintenance_data.description,
        "scheduled_date": maintenance.scheduled_date,
        "cost": maintenance.cost,
        "vendor": getattr(maintenance.vendor, 'id', None),
        "status": maintenance.status
    }

# ✅ Retrieve Asset by ID
@router.get("/{asset_id}", response_model=AssetSchema)
async def get_asset(asset_id: str):
    """
    Get Asset by Asset_id

    Example Asset_id : AST-8871

    URL : http://16.171.11.180/api/assets/AST-8871

    """ 
    asset = await Asset.get_or_none(asset_id=asset_id)
    print("Response data:", asset)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {
        "id": asset.id,
        "asset_id": asset.asset_id,
        "company": asset.company_id,
        "location": asset.location_id,
        "name": asset.name,
        "category": asset.category,
        "department": asset.department,
        "assigned": asset.assigned,
        "purchase_price": asset.purchase_price,
        "purchase_date": asset.purchase_date,
        "status": asset.status
    }