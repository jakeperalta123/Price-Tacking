from pydantic import BaseModel
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    unit: str
    price: float
    store: Optional[str] = None
    category: Optional[str] = None
    class Config:
        extra = "forbid"

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    store: Optional[str] = None

    class Config:
        extra = "forbid"