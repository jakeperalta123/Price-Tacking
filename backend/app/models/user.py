from sqlalchemy import String, TIMESTAMP, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import List
from .base import Base

class UserStatus:
    ACTIVE = "active"
    DISABLED = "disabled"
    DELETED = "deleted"
    ALL = {ACTIVE, DISABLED, DELETED}

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, server_default=text("'active'"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())

    products: Mapped[List["Product"]] = relationship(back_populates="user", cascade="save-update")
    __forbidden_update_fields__ = {"id", "password_hash", "created_at", "status"}
