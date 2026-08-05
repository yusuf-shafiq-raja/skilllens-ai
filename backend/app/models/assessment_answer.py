from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from sqlalchemy.orm import relationship

from app.database import Base


class AssessmentAnswer(Base):
    __tablename__ = "assessment_answers"

    id = Column(Integer, primary_key=True, index=True)

    attempt_id = Column(
        Integer,
        ForeignKey("assessment_attempts.id", ondelete="CASCADE"),
        nullable=False,
    )

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )

    # Stores only A / B / C / D
    selected_answer = Column(String(1), nullable=False)

    is_correct = Column(Boolean, default=False)

    marks_obtained = Column(Integer, default=0)

    attempt = relationship("AssessmentAttempt", back_populates="answers")

    question = relationship("Question", back_populates="attempt_answers")
