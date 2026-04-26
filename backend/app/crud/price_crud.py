from datetime import datetime, timezone, date
from sqlalchemy import select, update, func, text
from decimal import Decimal
from app.models.price import Price, PriceStatus
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

def create_price_entry(db: Session, product_id: int, price: Decimal, source: str):
    stmt = insert(Price).values(
        product_id=product_id,
        price=price,
        source=source,
        currency="USD",
        is_correction=False,
        status="active",
        created_at=datetime.now(),
        last_update=datetime.now()
    )

    stmt = stmt.on_conflict_do_nothing(
        index_elements=[
            'product_id',
            'price',
            'source',
            text("date_trunc('hour', created_at AT TIME ZONE 'UTC')")
        ]
    )

    try:
        result = db.execute(stmt)
        db.commit()
        return result
    except Exception as e:
        db.rollback()
        print(f"Database error: {e}")
        raise e

def get_today_active_price(product_id: int, start: datetime, end: datetime,  session: Session):
    return session.execute(
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.created_at >= start)
        .where(Price.created_at < end)
        .where(Price.status == PriceStatus.ACTIVE)
    ).scalar_one_or_none()

def get_product_latest_ten_price(session: Session, product_id: int, limit: int = 10):
    query = (
        select(Price)
        .where(Price.product_id == product_id)
        .where(Price.status == PriceStatus.ACTIVE)
        .order_by(Price.created_at.desc())
        .limit(limit)
    )

    result = session.execute(query).scalars().all()

    return result[::-1]

def create_price(product_id: int, price_value: Decimal, session: Session):
    price = Price(product_id = product_id, price = price_value, source="user")
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

    return {"average_price": average_price, "latest_price": latest_price}