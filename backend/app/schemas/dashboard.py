from pydantic import BaseModel


class DashboardResponse(BaseModel):

    user_name: str

    total_assessments: int

    completed_assessments: int

    average_score: float

    latest_score: float

    top_competency: str

    weakest_competency: str

    roadmap_priority: str

    resume_readiness: float