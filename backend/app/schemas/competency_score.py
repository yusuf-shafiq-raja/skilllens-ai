from datetime import datetime

from pydantic import BaseModel


class CompetencyScoreResponse(BaseModel):
    id: int

    competency_id: int

    questions_attempted: int

    correct_answers: int

    raw_score: float

    percentage: float

    level: str

    assessment_attempt_id: int

    created_at: datetime

    model_config = {
        "from_attributes": True
    }