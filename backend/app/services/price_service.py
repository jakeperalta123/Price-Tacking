from sqlalchemy.orm import Session
from app.crud.price_crud import get_recent_average_and_latest_price, get_product_latest_ten_price
from app.crud.product_crud import get_product_by_user_id
from datetime import datetime, timedelta

def get_latest_four_average_and_latest_price(user_id: int, session: Session, product_id: int | None = None):
    products = get_product_by_user_id(user_id, session)
    if product_id:
        products = [p for p in products if p.id == product_id]
    result = []
    for product in products:
        price_summary = get_recent_average_and_latest_price(product.id, session)
        result.append({"product_name": product.name, **price_summary})
    return result

def get_latest_ten_prices_by_product_id(user_id: int, product_id: int, session: Session):
    user_products = get_product_by_user_id(user_id, session)
    user_products_id = {p.id for p in user_products}

    if product_id not in user_products_id:
        raise ValueError("Unauthorized access to product data")

    prices = get_product_latest_ten_price(session, product_id)
    current_count = len(prices)
    target_count = 10

    if current_count < target_count:
        needed = target_count - current_count
        base_time = prices[0].created_at if prices else datetime.now()

        padding = []
        for i in range(needed):
            padding.append({
                "price": None, 
                "created_at": base_time - timedelta(minutes=(needed - i) * 10), 
                "is_virtual": True
            })
    return padding + prices
