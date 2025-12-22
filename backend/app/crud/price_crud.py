from datetime import datetime, timezone, date
from sqlalchemy import select, update, func
from models.price import Price
from sqlalchemy.orm import Session
from utils.db import safe_commit

def get_today_price(product_id: int, session: Session):
    today = date.today()
    return session.execute(
        select(Price)
        .where(Price.product_id == product_id)
        .where(func.date(Price.created_at) == today)
    ).scalar_one_or_none()

def create_price(product_id: int, price_value: float, session: Session):
    price = Price(product_id = product_id, price = price_value)
    session.add(price)
    return safe_commit(session, price)

def update_price(price: Price, new_price: float, session: Session):
    price.price = new_price
    price.last_update = func.now()
    return safe_commit(session, price)
