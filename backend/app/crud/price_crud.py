from datetime import datetime, timezone, date
from sqlalchemy import select, update, func
from decimal import Decimal
from app.models.price import Price, PriceStatus
from sqlalchemy.orm import Session

def get_today_active_price(product_id: int, start: datetime, end: datetime,  session: Session):
    return session.execute(
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.created_at >= start)
        .where(Price.created_at < end)
        .where(Price.status == PriceStatus.ACTIVE)
    ).scalar_one_or_none()

def create_price(product_id: int, price_value: Decimal, session: Session):
    price = Price(product_id = product_id, price = price_value)
    session.add(price)
    return price

def update_price(price: Price, new_price: Decimal, session: Session):
    corrected = Price(
        product_id=price.product_id, 
        price=new_price, 
        is_correction=True, 
        corrected_price_id=price.id
    )
    session.add(corrected)
    return corrected

def deactivate_price(price: Price):
    price.status = PriceStatus.ARCHIVED

def get_recent_average_and_latest_price(product_id: int, session: Session):
    
    recent_prices = session.execute(
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.status == PriceStatus.ACTIVE)
        .order_by(Price.created_at.desc())
        .limit(4)
    ).scalars().all()

    if not recent_prices:
        return {"average": None, "latest": None}
    
    total = sum(p.price for p in recent_prices)
    average_price = total / Decimal(len(recent_prices))
    latest_price = recent_prices[0].price

    return {"average price": average_price, "latest price": latest_price}