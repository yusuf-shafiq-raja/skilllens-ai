from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class PlacementReadiness(Base):
    __tablename__ = "placement_readiness"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    resume_score = Column(
        Float,
        default=0
    )

    assessment_score = Column(
        Float,
        default=0
    )

    competency_score = Column(
        Float,
        default=0
    )

    overall_score = Column(
        Float,
        default=0
    )

    readiness_level = Column(
        String(50),
        nullable=False
    )

    recommendation = Column(
        String(500),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    owner = relationship(
        "User"
    )