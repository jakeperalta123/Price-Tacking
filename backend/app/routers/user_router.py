from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.users import UserCreate, UserUpdate, PasswordUpdate
from app.crud.user_crud import createUser, updateUser, change_user_password
from app.db import getSession
from app.utils.security import get_current_user
from typing import Annotated
from app.models.user import User
from app.services.user_service import create_user_service, update_user_service, change_user_password_service

router = APIRouter(prefix="/users", tags=["users"])
common_session = Annotated[Session, Depends(getSession)]

# Security dependency for protected routes
auth_dependency = Annotated[User, Depends(get_current_user)]

@router.post("/register")
async def register_user(user_create: UserCreate, session: common_session):
    return create_user_service(user_create, session)

@router.patch("/update", dependencies=[Depends(get_current_user)])
async def update_user(user_update: UserUpdate, current_user: auth_dependency, session: common_session):
    return update_user_service(current_user.id, user_update, session)

@router.patch("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(payload: PasswordUpdate, current_user: auth_dependency, session: common_session):
    change_user_password_service(current_user.id, payload.current_password, payload.new_password, session)
    return