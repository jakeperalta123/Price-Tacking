from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import Session, declarative_base
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL") 
engine = create_engine(DATABASE_URL)

def getSession():
    with Session(engine) as session:
        yield session

sessionDep = Annotated[Session,Depends(getSession)]