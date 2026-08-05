from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database import Base


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    skill_id = Column(
        Integer, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )

    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    duration_minutes = Column(Integer, nullable=False)

    passing_score = Column(Integer, default=70)

    # NEW (Production Ready)
    max_attempts = Column(Integer, default=1)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="assessments")

    skill = relationship("Skill", back_populates="assessments")

    assessment_questions = relationship(
        "AssessmentQuestion", back_populates="assessment", cascade="all, delete-orphan"
    )

    attempts = relationship(
        "AssessmentAttempt", back_populates="assessment", cascade="all, delete-orphan"
    )
