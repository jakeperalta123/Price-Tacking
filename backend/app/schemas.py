from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None

    class Config:
        extra = "forbid"

class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str

    class Config:
        extra = "forbid"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    userid: int | None = None
