from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class ProductCreate(BaseModel):
    name: str
    unit: str
    price: Decimal
    store: Optional[str] = None
    category: Optional[str] = None
    class Config:
        extra = "forbid"
        json_encoders = {Decimal: lambda v: str(v)}

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[Decimal] = None
    store: Optional[str] = None

    class Config:
        extra = "forbid"
        json_encoders = {Decimal: lambda v: str(v)}