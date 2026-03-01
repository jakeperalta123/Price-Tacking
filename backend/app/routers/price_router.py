from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.security import get_current_user
from app.models.user import User
from app.db import getSession
from app.services.price_service import get_latest_four_average_and_latest_price, get_latest_ten_prices_by_product_id
from typing import Annotated, List
from fastapi.encoders import jsonable_encoder
from app.schemas.price import PriceHistoryResponse
from app.core.redis import redis_client

router = APIRouter(prefix="/prices", tags=["prices"])

@router.get("/latest-summary")
async def get_latest_summary(
    current_user: Annotated[User, Depends(get_current_user)], 
    session: Annotated[Session, Depends(getSession)], 
    product_id: int | None = None
    ):

    cache_key = f"user:{current_user.id}:summary"
    cached_data = await redis_client.get_cache(cache_key)

    if cached_data:
        print(f"cache hit! returning data for key: {cache_key}")
        return cached_data
    print(f"cache miss...")

    result = get_latest_four_average_and_latest_price(current_user.id, session, product_id)
    await redis_client.set_cache(cache_key, result, expire=3600)
    return jsonable_encoder(result)

@router.get("/history/{product_id}", response_model=List[PriceHistoryResponse])
async def get_product_latest_ten_price(
        product_id: int, 
        session: Annotated[Session, Depends(getSession)],
        current_user: Annotated[User, Depends(get_current_user)] 
):
    try:
        return get_latest_ten_prices_by_product_id(current_user.id, product_id, session)
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    