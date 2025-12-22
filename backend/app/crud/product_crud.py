from sqlalchemy.orm import Session
from schemas.products import ProductCreate, ProductUpdate
from sqlalchemy import select
from models.user import User, UserStatus
from models.product import Product
from fastapi import HTTPException

def get_product_by_user_id_and_name(user_id: int, product_name: str, session: Session):
    return session.execute(
        select(Product)
        .where(Product.name == product_name)
        .where(Product.user_id == user_id)
    ).scalar_one_or_none()

def create_product(user_id: int, product_name: str, product_category: str, session: Session):
    product = Product(user_id = user_id, name = product_name, category = product_category)
    try:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product
    except Exception:
        session.rollback()
        raise
        
    
    
    

