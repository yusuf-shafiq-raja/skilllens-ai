from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetencyScoreResponse(BaseModel):

    id: int

    competency_id: int

    assessment_attempt_id: int

    score: float

    total_questions: int

    correct_answers: int

    percentage: float

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )