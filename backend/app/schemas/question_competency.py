from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class QuestionCompetencyBase(BaseModel):
    question_id: int
    competency_id: int
    weight: float = 1.0


class QuestionCompetencyCreate(QuestionCompetencyBase):
    pass


class QuestionCompetencyUpdate(BaseModel):
    weight: Optional[float] = None


class QuestionCompetencyResponse(QuestionCompetencyBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}
