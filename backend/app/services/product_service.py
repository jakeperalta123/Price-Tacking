from crud.product_crud import get_product_by_user_id_and_name, create_product
from schemas.products import ProductCreate
from crud.user_crud import getActiveUserById
from crud.price_crud import get_today_price, create_price, update_price
from sqlalchemy.orm import Session
from fastapi import HTTPException

def upsert_today_price(user_id: int, product_data: ProductCreate, session: Session):
    product = get_product_by_user_id_and_name(user_id, product_data.name, session)
    if not product:
        product = create_product(user_id, product_data.name, product_data.category, session)
    
    today_price = get_today_price(product.id, session)

    if today_price:
        if today_price.last_update != today_price.created_at:
            raise HTTPException(status_code=400, detail="Price already corrected today")
        else:
            updated_price = update_price(today_price, product_data.price, session)
            return {"action": "updated", "price": updated_price.price, "product_id": product.id}
    else:
        new_price = create_price(product.id, product_data.price, session)
        return {"action": "created", "price": new_price.price, "product_id": product.id}
