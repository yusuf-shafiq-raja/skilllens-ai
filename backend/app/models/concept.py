from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum as SqlEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ConceptStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    skill_id = Column(
        Integer,
        ForeignKey("skills.id"),
        nullable=False
    )
    

    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=False)

    difficulty = Column(
        SqlEnum(DifficultyLevel),
        nullable=False
    )

    estimated_time = Column(
        Integer,
        nullable=False
    )

    learning_order = Column(
        Integer,
        nullable=False
    )

    status = Column(
        SqlEnum(ConceptStatus),
        default=ConceptStatus.NOT_STARTED,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner = relationship(
        "User",
        back_populates="concepts"
    )

    skill = relationship(
        "Skill",
        back_populates="concepts"
    )
    questions = relationship(
    "Question",
    back_populates="concept",
    cascade="all, delete-orphan"
    )
    
    