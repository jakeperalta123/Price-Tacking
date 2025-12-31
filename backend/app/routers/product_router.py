from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getSession
from typing import Annotated
from app.services.product_service import upsert_today_price
from app.schemas.products import ProductCreate
from app.utils.security import get_current_user
from app.models.user import User
from decimal import Decimal
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/products", tags=["products"])
common_session = Annotated[Session, Depends(getSession)]

@router.post("/price")
def create_or_update_price(
    product: ProductCreate,
    session: common_session,
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    result = upsert_today_price(current_user.id, product, session)
    return jsonable_encoder(result, custom_encoder={Decimal: str})

    
