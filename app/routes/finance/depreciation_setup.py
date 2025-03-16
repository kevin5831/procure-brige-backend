from fastapi import APIRouter, Depends, HTTPException
from app.models.depreciation import Depreciation
from app.schemas.depreciation import DepreciationSchema
from app.database import init_db

router = APIRouter(prefix='/depreciation-setup')

# 🚀 List & Create Companies
@router.get("/", response_model=list[DepreciationSchema])
async def list_depreciations():
    return await Depreciation.all()

@router.post("/", response_model=DepreciationSchema)
async def create_depreciation(depreciation_data: DepreciationSchema):
    depreciation = await Depreciation.create(**depreciation_data.dict())
    return depreciation

# 🚀 Get, Update & Delete a Depreciation
@router.get("/{depreciation_id}", response_model=DepreciationSchema)
async def get_depreciation(depreciation_id: int):
    depreciation = await Depreciation.get_or_none(id=depreciation_id)
    if not depreciation:
        raise HTTPException(status_code=404, detail="Depreciation not found")
    return depreciation

@router.put("/{depreciation_id}", response_model=DepreciationSchema)
async def update_depreciation(depreciation_id: int, depreciation_data: DepreciationSchema):
    depreciation = await Depreciation.get_or_none(id=depreciation_id)
    if not depreciation:
        raise HTTPException(status_code=404, detail="Depreciation not found")
    await depreciation.update_from_dict(depreciation_data.dict()).save()
    return depreciation

@router.delete("/{depreciation_id}")
async def delete_depreciation(depreciation_id: int):
    depreciation = await Depreciation.get_or_none(id=depreciation_id)
    if not depreciation:
        raise HTTPException(status_code=404, detail="Depreciation not found")
    await depreciation.delete()
    return {"message": "Depreciation deleted successfully"}

