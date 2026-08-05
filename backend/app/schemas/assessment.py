from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssessmentBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)

    description: str | None = Field(default=None, max_length=500)

    skill_id: int

    duration_minutes: int = Field(..., gt=0)

    passing_score: int = Field(..., ge=0, le=100)

    is_active: bool = True


class AssessmentCreate(AssessmentBase):
    pass


class AssessmentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)

    description: str | None = Field(default=None, max_length=500)

    skill_id: int | None = None

    duration_minutes: int | None = Field(default=None, gt=0)

    passing_score: int | None = Field(default=None, ge=0, le=100)

    is_active: bool | None = None


class AssessmentResponse(AssessmentBase):
    id: int
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
