from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    assessment_id = Column(
        Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
    )

    score = Column(Integer, default=0)

    total_marks = Column(Integer, default=0)

    percentage = Column(Float, default=0.0)

    status = Column(String, default="IN_PROGRESS")

    is_completed = Column(Boolean, default=False)

    time_taken_seconds = Column(Integer, default=0)

    started_at = Column(DateTime(timezone=True), server_default=func.now())

    submitted_at = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="assessment_attempts")

    assessment = relationship("Assessment", back_populates="attempts")

    answers = relationship(
        "AssessmentAnswer", back_populates="attempt", cascade="all, delete-orphan"
    )
    competency_scores = relationship(
        "CompetencyScore",
        back_populates="assessment_attempt",
        cascade="all, delete-orphan",
    )
