from sqlalchemy.orm import Session
from schemas.users import UserCreate
from utils.security import hashPwd, verify_password
from models.user import User, UserStatus
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from schemas.users import UserUpdate
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
import logging
from utils.db import safe_commit

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
logger = logging.getLogger(__name__)

def createUser(user: UserCreate, session: Session):
    existing_user = getUserAnyStatusByEmail(user.email, session)
    if existing_user:
        raise HTTPException(status_code=409, detail="User already exists")
    db_user = User(email=user.email, username=user.username, password_hash=hashPwd(user.password))
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return user
def getUserAnyStatusByEmail(email: str, session: Session):
    return session.execute(select(User).where(User.email == email)).scalar_one_or_none()
def getActiveUserByEmail(email: str, session: Session):
    return session.execute(select(User).where(User.email == email, User.status == UserStatus.ACTIVE)).scalar_one_or_none()
def getActiveUserById(user_id: int, session: Session):
    return session.execute(select(User).where(User.id == user_id, User.status == UserStatus.ACTIVE)).scalar_one_or_none()

def getUserAnyStatusById(user_id: int, session: Session):
    return session.execute(select(User).where(User.id == user_id)).scalar_one_or_none()

def getActiveUserByName(username: str, session: Session):
    return session.execute(select(User).where(User.username == username, User.status == UserStatus.ACTIVE)).scalar_one_or_none()

def getUserAnyStatusByName(username: str, session: Session):
    return session.execute(select(User).where(User.username == username)).scalar_one_or_none()

def updateUser(user_id: int, data: UserUpdate, session: Session):
    user = getActiveUserById(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_data = data.model_dump(exclude_unset=True)
    if "username" in update_data:
        existing = getUserAnyStatusByName(update_data["username"], session)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=409, detail="User name already in use")
    if "email" in update_data:
        existing = getUserAnyStatusByEmail(update_data["email"], session)
        if existing and existing.id != user_id:
            raise HTTPException(status_code=409, detail="Email already in use")
    forbidden_fields = getattr(User, "__forbidden_update_fields__", set())
    update_data = {k: v for k, v in update_data.items() if k not in forbidden_fields}

    for field, value in update_data.items():
        if hasattr(user, field):
            setattr(user, field, value)
    try: 
        safe_commit(session)
    except IntegrityError:
        session.rollback()
        raise HTTPException(status_code=409, detail="Conflict updating user")
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update user")
    return user


def authenticate_user(session: Session, email: str, password: str):
    user = getUserAnyStatusByEmail(email, session)
    if not user:
        logger.info(f"Log in attempt failed: user not found, email={email}")
        return None
    if user.status != UserStatus.ACTIVE:
        logger.info(f"Login attempt for non-active user: email={email}, status={user.status}")
        return None
    try:
        if not verify_password(password, user.password_hash):
            logger.info(f"Login attempt failed: incorrect password, email={email}")
            return None
    except Exception:
        logger.exception(f"Error verifying password for email={email}")
        return None
    return user
    

def change_user_password(user_id: int, current_password: str, new_password: str, session: Session):
    user = getActiveUserById(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        if not verify_password(current_password, user.password_hash):
            raise HTTPException(status_code=401, detail="Incorrect user password")
    except Exception:
        raise HTTPException(status_code=401, detail="Incorrect current password")
    
    if len(new_password) < 8:
        raise HTTPException(status_code=400, detail="Password too weak")
    
    user.password_hash = hashPwd(new_password)

    try:
        session.commit()
        session.refresh(user)
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Failed to update password")
    
    return


    