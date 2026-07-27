from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

from app.models.user import User
from app.models.skill import Skill
from app.models.concept import Concept

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()