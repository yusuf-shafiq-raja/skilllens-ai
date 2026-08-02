from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    competency_id = Column(
        Integer,
        ForeignKey(
            "competencies.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    title = Column(
        String(150),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    study_topics = Column(
        Text,
        nullable=False
    )

    practice_tasks = Column(
        Text,
        nullable=False
    )

    next_learning = Column(
        String(150),
        nullable=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    competency = relationship(
        "Competency",
        back_populates="roadmaps"
    )