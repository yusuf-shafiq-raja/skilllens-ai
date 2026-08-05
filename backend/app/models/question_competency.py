from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class QuestionCompetency(Base):
    __tablename__ = "question_competencies"

    id = Column(Integer, primary_key=True, index=True)

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )

    competency_id = Column(
        Integer, ForeignKey("competencies.id", ondelete="CASCADE"), nullable=False
    )

    weight = Column(Float, default=1.0, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships

    question = relationship("Question", back_populates="question_competencies")

    competency = relationship("Competency", back_populates="question_competencies")
