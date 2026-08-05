from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict

# ---------------------------------------------------------
# Placement Readiness Response
# ---------------------------------------------------------


class PlacementReadinessResponse(BaseModel):

    id: int

    user_id: int

    resume_score: float

    assessment_score: float

    competency_score: float

    overall_score: float

    readiness_level: str

    recommendation: str

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
