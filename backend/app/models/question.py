from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class QuestionType(str, Enum):
    MCQ = "MCQ"
    TRUE_FALSE = "True/False"


class AnswerOption(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)

    question = Column(Text, nullable=False)

    option_a = Column(String(255), nullable=False)

    option_b = Column(String(255), nullable=False)

    option_c = Column(String(255), nullable=False)

    option_d = Column(String(255), nullable=False)

    correct_answer = Column(SqlEnum(AnswerOption), nullable=False)

    explanation = Column(Text, nullable=False)

    difficulty = Column(SqlEnum(DifficultyLevel), nullable=False)

    question_type = Column(
        SqlEnum(QuestionType), default=QuestionType.MCQ, nullable=False
    )

    marks = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="questions")

    concept = relationship("Concept", back_populates="questions")
    assessment_questions = relationship(
        "AssessmentQuestion", back_populates="question", cascade="all, delete-orphan"
    )
    attempt_answers = relationship(
        "AssessmentAnswer", back_populates="question", cascade="all, delete-orphan"
    )
    question_competencies = relationship(
        "QuestionCompetency", back_populates="question", cascade="all, delete-orphan"
    )
