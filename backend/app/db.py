from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# this reads .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# an engine, which the session will use for connection resources
engine = create_engine(DATABASE_URL)

# sessionmaker is like a firm, you can hire people(session) from this firm, 
# and use session to interact with DB through connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()