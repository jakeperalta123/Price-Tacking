from app.models.base import Base
from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:test123@localhost:3306/price_tracker"
engine = create_engine(DATABASE_URL)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully with version column")