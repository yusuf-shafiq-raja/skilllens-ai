from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User
from app.schemas.competency_score import CompetencyScoreResponse

from app.services.competency_score_service import (
    get_competency_scores_by_attempt,
    get_latest_competency_scores,
    get_competency_score_history
)

router = APIRouter(
    prefix="/competency-scores",
    tags=["Competency Scores"]
)


# ---------------------------------------------------------
# Get Scores by Assessment Attempt
# ---------------------------------------------------------

@router.get(
    "/attempt/{attempt_id}",
    response_model=list[CompetencyScoreResponse]
)
def get_scores_by_attempt(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_competency_scores_by_attempt(
            db,
            attempt_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ---------------------------------------------------------
# Latest Competency Scores
# ---------------------------------------------------------

@router.get(
    "/latest",
    response_model=list[CompetencyScoreResponse]
)
def latest_scores(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_latest_competency_scores(
            db,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ---------------------------------------------------------
# Competency Score History
# ---------------------------------------------------------

@router.get(
    "/history",
    response_model=list[CompetencyScoreResponse]
)
def competency_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_competency_score_history(
        db,
        current_user
    )