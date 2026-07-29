from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)

from sqlalchemy.orm import relationship

from app.database import Base


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    assessment_id = Column(
        Integer,
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    marks = Column(
        Integer,
        nullable=False,
        default=1,
    )

    assessment = relationship(
        "Assessment",
        back_populates="assessment_questions",
    )

    question = relationship(
        "Question",
        back_populates="assessment_questions",
    )