from pydantic import BaseModel
from datetime import datetime


class SkillCreate(BaseModel):
    name: str
    description: str
    category: str


class SkillUpdate(BaseModel):
    name: str
    description: str
    category: str


class SkillResponse(BaseModel):
    id: int
    name: str
    description: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True
