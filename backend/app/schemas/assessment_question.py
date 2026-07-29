from pydantic import BaseModel, ConfigDict, Field


class AssessmentQuestionCreate(BaseModel):
    question_ids: list[int] = Field(..., min_length=1)


class AssessmentQuestionResponse(BaseModel):
    id: int

    assessment_id: int

    question_id: int

    marks: int

    model_config = ConfigDict(from_attributes=True)