from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"


class ConceptStatus(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


class ConceptBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=500)
    difficulty: DifficultyLevel
    estimated_time: int = Field(..., gt=0)
    learning_order: int = Field(..., gt=0)


class ConceptCreate(ConceptBase):
    skill_id: int


class ConceptUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    description: str | None = Field(default=None, min_length=5, max_length=500)
    difficulty: DifficultyLevel | None = None
    estimated_time: int | None = Field(default=None, gt=0)
    learning_order: int | None = Field(default=None, gt=0)
    status: ConceptStatus | None = None


class ConceptResponse(ConceptBase):
    id: int
    user_id: int
    skill_id: int
    status: ConceptStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)