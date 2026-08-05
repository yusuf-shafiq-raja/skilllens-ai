from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class AssessmentInfo(BaseModel):
    id: int
    title: str
    description: str | None = None
    duration_minutes: int
    passing_score: int

    class Config:
        from_attributes = True


class QuestionForAttempt(BaseModel):
    id: int

    question: str

    option_a: str
    option_b: str
    option_c: str
    option_d: str

    marks: int

    class Config:
        from_attributes = True


class StartAssessmentResponse(BaseModel):

    attempt_id: int

    started_at: datetime

    assessment: AssessmentInfo

    questions: List[QuestionForAttempt]


class AssessmentAttemptDetailsResponse(BaseModel):

    attempt_id: int

    started_at: datetime

    assessment: AssessmentInfo

    questions: List[QuestionForAttempt]


class AssessmentResultResponse(BaseModel):

    id: int

    assessment_id: int

    score: int

    total_marks: int

    percentage: float

    status: str

    started_at: datetime

    submitted_at: Optional[datetime]

    class Config:
        from_attributes = True
