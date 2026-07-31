from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String(255),
        nullable=False
    )

    skills = relationship(
        "Skill",
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    concepts = relationship(
    "Concept",
    back_populates="owner",
    cascade="all, delete-orphan"
    )
    questions = relationship(
    "Question",
    back_populates="owner",
    cascade="all, delete-orphan"
    )
    assessments = relationship(
    "Assessment",
    back_populates="owner",
    cascade="all, delete-orphan"
    )
    assessment_attempts = relationship(
    "AssessmentAttempt",
    back_populates="owner",
    cascade="all, delete-orphan"
    )
    competency_scores = relationship(
    "CompetencyScore",
    back_populates="owner",
    cascade="all, delete-orphan"
)