from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.crud.user_crud import authenticate_user
from app.utils.security import create_access_token
from app.db import getSession
from datetime import timedelta
from typing import Annotated
from app.schemas.tokens import Token
from dotenv import load_dotenv
import os
from app.models.user import UserStatus

load_dotenv()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],session: Annotated[Session, Depends(getSession)]
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password",headers={"WWW-Authenticate": "Bearer"},)
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="User account is inactive")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
