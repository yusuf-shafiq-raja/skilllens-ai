from typing import List

from pydantic import BaseModel


class RoadmapItem(BaseModel):

    competency: str

    current_level: str

    percentage: float

    priority: int

    estimated_hours: int

    recommended_concepts: List[str]


class RoadmapResponse(BaseModel):

    roadmap: List[RoadmapItem]