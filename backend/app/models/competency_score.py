from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class CompetencyScore(Base):
    __tablename__ = "competency_scores"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    competency_id = Column(
        Integer,
        ForeignKey("competencies.id", ondelete="CASCADE"),
        nullable=False
    )

    assessment_attempt_id = Column(
        Integer,
        ForeignKey("assessment_attempts.id", ondelete="CASCADE"),
        nullable=False
    )

    score = Column(
        Float,
        default=0,
        nullable=False
    )

    total_questions = Column(
        Integer,
        default=0,
        nullable=False
    )

    correct_answers = Column(
        Integer,
        default=0,
        nullable=False
    )

    percentage = Column(
        Float,
        default=0,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner = relationship(
        "User",
        back_populates="competency_scores"
    )

    competency = relationship(
        "Competency",
        back_populates="competency_scores"
    )

    assessment_attempt = relationship(
        "AssessmentAttempt",
        back_populates="competency_scores"
    )