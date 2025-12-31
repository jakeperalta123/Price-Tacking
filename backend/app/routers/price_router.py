from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.security import get_current_user
from app.models.user import User
from app.db import getSession
from app.services.price_service import get_latest_four_average_and_latest_price
from typing import Annotated
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/prices", tags=["prices"])

@router.get("/latest-summary")
async def get_latest_summary(
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(getSession)], 
    product_id: int | None = None
    ):

    result = get_latest_four_average_and_latest_price(current_user.id, session, product_id)
    return jsonable_encoder(result)