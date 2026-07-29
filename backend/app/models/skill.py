from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    category = Column(String(100), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner = relationship("User", back_populates="skills")
    concepts = relationship(
    "Concept",
    back_populates="skill",
    cascade="all, delete-orphan"
    )
    assessments = relationship(
    "Assessment",
    back_populates="skill",
    cascade="all, delete-orphan"
    )