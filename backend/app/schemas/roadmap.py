from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RoadmapBase(BaseModel):

    competency_id: int

    title: str

    description: Optional[str] = None

    study_topics: str

    practice_tasks: str

    next_learning: Optional[str] = None

    is_active: bool = True


class RoadmapCreate(RoadmapBase):
    pass


class RoadmapUpdate(BaseModel):

    competency_id: Optional[int] = None

    title: Optional[str] = None

    description: Optional[str] = None

    study_topics: Optional[str] = None

    practice_tasks: Optional[str] = None

    next_learning: Optional[str] = None

    is_active: Optional[bool] = None


class RoadmapResponse(RoadmapBase):

    id: int

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
