# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.models.base import Base

# Get database URL from environment variable or use default
POSTGRES_URL = os.getenv("DATABASE_URL", "postgresql://tiss_user:tiss_password@localhost:5432/tiss")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()