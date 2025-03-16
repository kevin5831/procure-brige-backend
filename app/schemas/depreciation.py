from pydantic import BaseModel, EmailStr
from typing import Optional

class DepreciationSchema(BaseModel):
    category: str
    residual_value: int
    useful_life_ifrs: int
    useful_life_tax: int

    class Config:
        from_attributes = True