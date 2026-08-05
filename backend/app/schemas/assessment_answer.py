from pydantic import BaseModel, ConfigDict


class AssessmentAnswerCreate(BaseModel):
    question_id: int
    selected_answer: str


class AssessmentAnswerResponse(BaseModel):
    id: int

    attempt_id: int

    question_id: int

    selected_answer: str

    is_correct: bool

    marks_obtained: int

    model_config = ConfigDict(from_attributes=True)
