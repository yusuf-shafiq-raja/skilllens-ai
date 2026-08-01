from typing import List

from pydantic import BaseModel


# ---------------------------------------------------------
# Resume Analysis Response
# ---------------------------------------------------------

class ResumeAnalysisResponse(BaseModel):

    matched_skills: List[str]

    missing_skills: List[str]

    matched_count: int

    missing_count: int

    readiness_score: float

    extracted_text: str