from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.roadmap import RoadmapResponse

from app.services.roadmap_service import (
    get_latest_roadmap,
    get_roadmap_by_attempt
)

router = APIRouter(
    prefix="/roadmap",
    tags=["Learning Roadmap"]
)


# ---------------------------------------------------------
# Latest Roadmap
# ---------------------------------------------------------

@router.get(
    "/latest",
    response_model=RoadmapResponse
)
def latest_roadmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_latest_roadmap(
            db,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ---------------------------------------------------------
# Roadmap by Attempt
# ---------------------------------------------------------

@router.get(
    "/{attempt_id}",
    response_model=RoadmapResponse
)
def roadmap_by_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_roadmap_by_attempt(
            db,
            attempt_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )