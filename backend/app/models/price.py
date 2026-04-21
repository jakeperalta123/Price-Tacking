from sqlalchemy import Numeric, String, ForeignKey, TIMESTAMP, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base
from decimal import Decimal

class PriceStatus:
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    ALL = {ACTIVE, ARCHIVED, DELETED}
class Price(Base):
    __tablename__ = "prices"

    id: Mapped[int]  = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2, asdecimal=True), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), index=True)
    last_update: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    is_correction: Mapped[bool] = mapped_column(default=False)
    corrected_price_id: Mapped[int] = mapped_column(ForeignKey("prices.id"), nullable=True)
    product: Mapped["Product"] = relationship(back_populates="prices")
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default="active")
    source: Mapped[str] = mapped_column(String(20), nullable=False, server_default="user", default="user")
    __table_args__ = (
        Index('idx_product_status_created', 'product_id', 'status', 'created_at'), 
    )