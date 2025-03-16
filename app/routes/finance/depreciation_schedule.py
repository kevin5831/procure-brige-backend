from fastapi import APIRouter, HTTPException
from app.models.depreciation import Depreciation
from app.models.depreciation_history import DepreciationHistory
from app.models.assets import Asset
from app.database import init_db
import datetime
router = APIRouter(prefix='/depreciation-schedule')

# 🚀 All Assets Annually and Monthly Depreciation
@router.get("/")
async def list_depreciations_schedule():
    data = []    
    depreciation_data = []    
    currentDate = datetime.datetime.now()
    assets = await Asset.all()
    for asset in assets:
        annual_depreciation_ifrs = []
        monthly_depreciation_ifrs = []
        annual_depreciation_tax = []
        monthly_depreciation_tax = []
        depreciation = await Depreciation.get_or_none(category=asset.category)     
        if not depreciation:
            raise HTTPException(status_code=404, detail="Depreciation not found")
        
        purchase_price = asset.purchase_price        
        residual_value = depreciation.residual_value
        useful_life_ifrs = int(depreciation.useful_life_ifrs)
        depreciation_rate_ifrs = 2 / useful_life_ifrs
        useful_life_tax = int(depreciation.useful_life_tax)
        depreciation_rate_tax = 2 / useful_life_tax
        if asset.depreciation_method == "straight_line":
            annual_depreciation_ifrs_value = (purchase_price - residual_value) / useful_life_ifrs
            for i in range(useful_life_ifrs):
                annual_depreciation_ifrs.append({f"{i+1}_year": round(annual_depreciation_ifrs_value, 2)})
                monthly_depreciation_ifrs.append({f"{i+1}_month": round(annual_depreciation_ifrs_value / 12, 2)})
            annual_depreciation_tax_value = (purchase_price - residual_value) / useful_life_tax
            for i in range(useful_life_tax):
                annual_depreciation_tax.append({f"{i+1}_year": round(annual_depreciation_tax_value, 2)})
                monthly_depreciation_tax.append({f"{i+1}_month": round(annual_depreciation_tax_value / 12, 2)})

        else :
            for i in range(useful_life_ifrs):
                annual_depreciation_ifrs_value = purchase_price * depreciation_rate_ifrs / useful_life_ifrs
                purchase_price = purchase_price - annual_depreciation_ifrs_value
                annual_depreciation_ifrs.append({f"{i}year": round(annual_depreciation_ifrs_value, 2)})
                monthly_depreciation_ifrs.append({f"{i}month": round(annual_depreciation_ifrs_value / 12, 2)})
            for i in range(useful_life_tax):
                annual_depreciation_tax_value = purchase_price * depreciation_rate_tax / useful_life_tax
                purchase_price = purchase_price - annual_depreciation_tax_value
                annual_depreciation_tax.append({f"{i}year": round(annual_depreciation_tax_value, 2)})
                monthly_depreciation_tax.append({f"{i}month": round(annual_depreciation_tax_value / 12, 2)})

        data.append({
            "asset_name": asset.name,
            "asset_category": asset.category,
            "depreciation_method": asset.depreciation_method,
            "depreciation_ifrs": {
                "annual_depreciation_ifrs": annual_depreciation_ifrs,
                "monthly_depreciation_ifrs": monthly_depreciation_ifrs
            },
            "depreciation_tax": {
                "annual_depreciation_tax": annual_depreciation_tax,
                "monthly_depreciation_tax": monthly_depreciation_tax
            }  
        })
        depreciation_data.append({
            "asset_id": asset.id,
            "update_date": asset.purchase_date,
            "update_date": currentDate
        })
    await DepreciationHistory.create(depreciation_data)
    
    return data

# 🚀 Asset Annually and Monthly Depreciation
@router.get("/{asset_id}")
async def depreciation_schedule(asset_id: int):
    asset = await Asset.get_or_none(id=asset_id)
    data=[]
    depreciation_data = []    
    annual_depreciation_ifrs = []
    monthly_depreciation_ifrs = []
    annual_depreciation_tax = []
    monthly_depreciation_tax = []
    currentDate = datetime.datetime.now()
    depreciation = await Depreciation.get_or_none(category=asset.category)     
    if not depreciation:
        raise HTTPException(status_code=404, detail="Depreciation not found")
    
    purchase_price = asset.purchase_price
    residual_value = depreciation.residual_value
    useful_life_ifrs = int(depreciation.useful_life_ifrs)    
    depreciation_rate_ifrs = 2 / useful_life_ifrs
    useful_life_tax = int(depreciation.useful_life_tax)
    depreciation_rate_tax = 2 / useful_life_tax
    if asset.depreciation_method == "straight_line":
        annual_depreciation_ifrs_value = (purchase_price - residual_value) / useful_life_ifrs
        for i in range(useful_life_ifrs):
            annual_depreciation_ifrs.append({"annual": round(annual_depreciation_ifrs_value, 2)})
            monthly_depreciation_ifrs.append({"monthly": round(annual_depreciation_ifrs_value / 12, 2)})
        annual_depreciation_tax_value = (purchase_price - residual_value) / useful_life_tax
        for i in range(useful_life_tax):
            annual_depreciation_tax.append({f"{i+1}_year": round(annual_depreciation_tax_value, 2)})
            monthly_depreciation_tax.append({f"{i+1}_month": round(annual_depreciation_tax_value / 12, 2)})

    else :
        for i in range(useful_life_ifrs):
            annual_depreciation_ifrs_value = purchase_price * depreciation_rate_ifrs / useful_life_ifrs
            purchase_price = purchase_price - annual_depreciation_ifrs_value
            annual_depreciation_ifrs.append({"annual": round(annual_depreciation_ifrs_value, 2)})
            monthly_depreciation_ifrs.append({"monthly": round(annual_depreciation_ifrs_value / 12, 2)})
        for i in range(useful_life_tax):
            annual_depreciation_tax_value = purchase_price * depreciation_rate_tax / useful_life_tax
            purchase_price = purchase_price - annual_depreciation_tax_value
            annual_depreciation_tax.append({f"{i}year": round(annual_depreciation_tax_value, 2)})
            monthly_depreciation_tax.append({f"{i}month": round(annual_depreciation_tax_value / 12, 2)})

    data.append({
        "asset_name": asset.name,
        "asset_category": asset.category,
        "depreciation_method": asset.depreciation_method,
        "depreciation_ifrs": {
            "annual_depreciation_ifrs": annual_depreciation_ifrs,
            "monthly_depreciation_ifrs": monthly_depreciation_ifrs
        },
        "depreciation_tax": {
            "annual_depreciation_tax": annual_depreciation_tax,
            "monthly_depreciation_tax": monthly_depreciation_tax
        }      
    })      
    depreciation_data.append({
        "asset_id": asset.id,
        "update_date": asset.purchase_date,
        "update_date": currentDate
    })
    history = await DepreciationHistory.get_or_none(id=asset.id)
    return history

