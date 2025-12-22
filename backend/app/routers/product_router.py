from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import getSession
from typing import Annotated
from services.product_service import upsert_today_price
from schemas.products import ProductCreate
from utils.security import get_current_user
from models.user import User

router = APIRouter(prefix="/products", tags=["products"])
common_session = Annotated[Session, Depends(getSession)]

@router.post("/price")
def create_or_update_price(
    product: ProductCreate, 
    session: common_session, 
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    result = upsert_today_price(current_user.id, product, session)
    return result

