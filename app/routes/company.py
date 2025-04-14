from fastapi import APIRouter, Depends, HTTPException
from app.models.company import Company, Location, Department, Invitation
from app.schemas.company import CompanySchema, LocationSchema, DepartmentSchema, InvitationSchema
from app.database import init_db

router = APIRouter()

# 🚀 List & Create Companies
@router.get("/", response_model=list[CompanySchema])
async def list_companies():
    """
    Get All Company List

    URL : http://16.171.11.180/companies/

    """ 
    return await Company.all()

@router.post("/", response_model=CompanySchema)
async def create_company(company_data: CompanySchema):
    company = await Company.create(**company_data.dict())
    return company

# 🚀 Get, Update & Delete a Company
@router.get("/{company_id}", response_model=CompanySchema)
async def get_company(company_id: int):
    company = await Company.get_or_none(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanySchema)
async def update_company(company_id: int, company_data: CompanySchema):
    company = await Company.get_or_none(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    await company.update_from_dict(company_data.dict()).save()
    return company

@router.delete("/{company_id}")
async def delete_company(company_id: int):
    company = await Company.get_or_none(id=company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    await company.delete()
    return {"message": "Company deleted successfully"}

@router.post("/location", response_model=LocationSchema)
async def create_location(location_data: LocationSchema):
    company = await Company.get(id=location_data.company)
    location = await Location.create(
        company=company,
        name=location_data.name,
        code= location_data.code,
        location_type=location_data.location_type,
        country=location_data.country,
        city=location_data.city,
        address=location_data.address
    )
    return {
        "company":company.id,
        "name":location_data.name,
        "code": location_data.code,
        "location_type":location_data.location_type,
        "country":location_data.country,
        "city":location_data.city,
        "address":location_data.address
    }

# 🚀 List Locations by Company
@router.get("/{company_id}/locations", response_model=list[LocationSchema])
async def list_locations(company_id: int):
    """
    Get All Location List via company_id

    URL : http://16.171.11.180/companies/{company_id}/locations

    """ 
    locations = await Location.filter(company_id=company_id)
    
    result = []
    for location in locations:
        result.append({
            "id": location.id,
            "company": location.company_id,  # Use company_id instead of company
            "name": location.name,
            "code": location.code,
            "location_type": location.location_type,
            "country": location.country,
            "city": location.city,
            "address": location.address
        })
    
    return result

# 🚀 List Departments by Company
@router.get("/{company_id}/departments", response_model=list[DepartmentSchema])
async def list_departments(company_id: int):
    return await Department.filter(company_id=company_id)

# 🚀 List Invitations by Company
@router.get("/{company_id}/invitations", response_model=list[InvitationSchema])
async def list_invitations(company_id: int):
    return await Invitation.filter(company_id=company_id)
