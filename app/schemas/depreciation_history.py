from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date

class DepreciationHistorySchema(BaseModel):
    asset_id: int
    depreciation: str
    update_date: date

    class Config:
        from_attributes = True