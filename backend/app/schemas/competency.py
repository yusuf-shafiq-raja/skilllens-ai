from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CompetencyBase(BaseModel):
    name: str
    description: Optional[str] = None
    skill_id: int
    is_active: bool = True


class CompetencyCreate(CompetencyBase):
    pass


class CompetencyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    skill_id: Optional[int] = None
    is_active: Optional[bool] = None


class CompetencyResponse(CompetencyBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }