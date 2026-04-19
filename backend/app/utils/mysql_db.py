from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends

load_dotenv()

MYSQL_URL = os.getenv("MYSQL_URL")
engine = create_engine(MYSQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_mysql_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

mysqlSessionDep = Annotated[Session, Depends(get_mysql_session)]