from app.crud.product_crud import get_product_by_user_id_and_name, create_product
from app.schemas.products import ProductCreate
from app.crud.user_crud import getActiveUserById
from app.crud.price_crud import get_today_active_price, create_price, update_price, deactivate_price
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta

def upsert_today_price(user_id: int, product_data: ProductCreate, session: Session):
    product = get_product_by_user_id_and_name(user_id, product_data.name, session)
    if not product:
        product = create_product(user_id, product_data.name, product_data.category, session)
        
    today_start = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0)
    tomorrow_start = today_start + timedelta(days=1)
    today_price = get_today_active_price(product.id, today_start, tomorrow_start, session)

    if today_price:
        if today_price.is_correction:
            raise HTTPException(status_code=400, detail="Price already corrected today")
        else:
            deactivate_price(today_price)
            updated_price = update_price(today_price, product_data.price, session)
            result = {"action": "updated", "price": updated_price.price, "product_id": product.id}
    else:
        new_price = create_price(product.id, product_data.price, session)
        result = {"action": "created", "price": new_price.price, "product_id": product.id}
    session.commit()
    return result

