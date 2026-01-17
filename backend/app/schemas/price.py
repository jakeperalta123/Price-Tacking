from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class PriceHistoryResponse(BaseModel):
    price: Optional[Decimal]
    created_at: datetime
    is_virtual: bool = False
    
    class Config:
        from_attributes = True