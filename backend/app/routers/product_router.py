from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import getSession
from typing import Annotated
from app.services.product_service import upsert_today_price, check_and_trigger_monitoring
from app.schemas.products import ProductCreate
from app.utils.security import get_current_user
from app.models.user import User
from decimal import Decimal
from fastapi.encoders import jsonable_encoder
from app.api.deps import get_redis
from app.core.redis import RedisCache

router = APIRouter(prefix="/products", tags=["products"])
common_session = Annotated[Session, Depends(getSession)]

@router.post("/price")
async def create_or_update_price(
    product: ProductCreate,
    session: common_session,
    current_user: Annotated[User, Depends(get_current_user)], 
    redis: Annotated[RedisCache, Depends(get_redis)]
    ):

    result = upsert_today_price(current_user.id, product, session)
    is_triggered, count = await check_and_trigger_monitoring(current_user.id, product.name, session, redis=redis)

    cache_key = f"user:{current_user.id}:summary"
    await redis.delete_cache(cache_key)

    msg = "已開啟每日監控！ " if is_triggered else f"已紀錄，目前次數:{count}"
    response_data = {
        "status": "success", 
        "message": msg, 
        "data": result
    }

    return jsonable_encoder(
        response_data, custom_encoder={Decimal: str}
        )

    
