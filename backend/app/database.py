from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL)

# Create Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all database models
Base = declarative_base()
from app.models.user import User
from app.models.skill import Skill

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()