from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import Session, sessionmaker
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def getSession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

sessionDep = Annotated[Session,Depends(getSession)]