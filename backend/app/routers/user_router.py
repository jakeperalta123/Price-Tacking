from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, UserUpdate
from crud.user_crud import createUser, updateUser
from db import getSession
from utils.security import get_current_user
from typing import Annotated
from models.user import User

router = APIRouter(prefix="/users", tags=["users"])
commonSession = Annotated[Session, Depends(getSession)]

# Security dependency for protected routes
auth_dependency = Annotated[User, Depends(get_current_user)]

@router.post("/register")
async def register_user(user_create: UserCreate, session: commonSession):
    return createUser(user_create, session)

@router.patch("/update", dependencies=[Depends(get_current_user)])
async def update_user(user_update: UserUpdate, current_user: auth_dependency, session: commonSession):
    return updateUser(current_user.id, user_update, session)
