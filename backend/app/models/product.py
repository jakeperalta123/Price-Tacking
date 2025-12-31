from sqlalchemy import String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List, Optional
from app.models.base import Base

class ProductStatus:
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    ALL = {ACTIVE, ARCHIVED, DELETED}
    
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")
    user: Mapped["User"] = relationship(back_populates="products")
    prices: Mapped[List["Price"]] = relationship(back_populates="product", cascade="all, delete-orphan")
