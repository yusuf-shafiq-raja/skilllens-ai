from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Competency(Base):
    __tablename__ = "competencies"

    id = Column(Integer, primary_key=True, index=True)

    skill_id = Column(
        Integer,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String(100), nullable=False)

    description = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    # Relationships

    skill = relationship(
        "Skill",
        back_populates="competencies"
    )
    question_competencies = relationship(
    "QuestionCompetency",
    back_populates="competency",
    cascade="all, delete-orphan"
)


    
    competency_scores = relationship(
        "CompetencyScore",
        back_populates="competency",
        cascade="all, delete-orphan"
    )