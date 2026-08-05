from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


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


class QuestionBase(BaseModel):
    question: str = Field(..., min_length=10)

    option_a: str = Field(..., min_length=1)
    option_b: str = Field(..., min_length=1)
    option_c: str = Field(..., min_length=1)
    option_d: str = Field(..., min_length=1)

    correct_answer: AnswerOption

    explanation: str = Field(..., min_length=5)

    difficulty: DifficultyLevel

    question_type: QuestionType = QuestionType.MCQ

    marks: int = Field(..., gt=0)


class QuestionCreate(QuestionBase):
    concept_id: int


class QuestionUpdate(BaseModel):
    question: str | None = None

    option_a: str | None = None
    option_b: str | None = None
    option_c: str | None = None
    option_d: str | None = None

    correct_answer: AnswerOption | None = None

    explanation: str | None = None

    difficulty: DifficultyLevel | None = None

    question_type: QuestionType | None = None

    marks: int | None = Field(default=None, gt=0)


class QuestionResponse(QuestionBase):
    id: int
    user_id: int
    concept_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
