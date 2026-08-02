from typing import List

from pydantic import BaseModel


class RecommendedAssessment(BaseModel):

    id: int

    title: str

    description: str

    duration_minutes: int

    passing_score: int


class ResumeAnalysisResponse(BaseModel):

    matched_skills: List[str]

    missing_skills: List[str]

    matched_count: int

    missing_count: int

    readiness_score: float

    extracted_text: str

    recommended_assessments: List[RecommendedAssessment]