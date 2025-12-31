from sqlalchemy.orm import Session
from app.crud.price_crud import get_recent_average_and_latest_price
from app.crud.product_crud import get_product_by_user_id

def get_latest_four_average_and_latest_price(user_id: int, session: Session, product_id: int | None = None):
    products = get_product_by_user_id(user_id, session)
    if product_id:
        products = [p for p in products if p.id == product_id]
    result = []
    for product in products:
        price_summary = get_recent_average_and_latest_price(product.id, session)
        result.append({"product_name": product.name, **price_summary})
    return result