from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.placement_readiness import PlacementReadinessResponse

from app.services.placement_readiness_service import (
    generate_placement_readiness,
    get_placement_readiness,
)

router = APIRouter(prefix="/placement-readiness", tags=["Placement Readiness"])


# ---------------------------------------------------------
# Generate Placement Readiness
# ---------------------------------------------------------


@router.post("/generate/{resume_score}", response_model=PlacementReadinessResponse)
def generate_readiness(
    resume_score: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return generate_placement_readiness(db, current_user, resume_score)


# ---------------------------------------------------------
# Get Placement Readiness
# ---------------------------------------------------------


@router.get("/", response_model=PlacementReadinessResponse)
def get_readiness(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    try:

        return get_placement_readiness(db, current_user)

    except ValueError as e:

        raise HTTPException(status_code=404, detail=str(e))
