from typing import List

from pydantic import BaseModel


class LearningRoadmapResponse(BaseModel):

    competency: str

    percentage: float

    level: str

    study_topics: List[str]

    practice_tasks: List[str]

    next_learning: str
