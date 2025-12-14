from sqlalchemy.orm import Session
from schemas import UserCreate
from utils.security import hashPwd
from models.user import User
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from schemas import UserUpdate
from sqlalchemy import select
import bcrypt

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def createUser(user: UserCreate, session: Session):
    existing_user = getUserByEmail(user.email, session)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    db_user = User(email=user.email, username=user.username, password_hash=hashPwd(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return user

def getUserByEmail(email, session: Session):
    return session.execute(select(User).where(User.email == email)).scalar_one_or_none()

def updateUser(user_id: int, data: UserUpdate, session: Session):
    user = session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.model_dump(exclude_unset=True)
    forbidden_fields = getattr(User, "__forbidden_update_fields__", set())
    update_data = {k: v for k, v in update_data.items() if k not in forbidden_fields}

    for field, value in update_data.items():
        setattr(user, field, value)
    
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = getUserByEmail(email, session)
    if not user:
        return None
    try:
        if not bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return None
    except Exception:
        return None
    return user
    

