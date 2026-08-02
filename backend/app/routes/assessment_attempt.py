from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.assessment_attempt import (
    StartAssessmentResponse,
    AssessmentResultResponse
)

from app.schemas.assessment_answer import (
    AssessmentAnswerCreate,
    AssessmentAnswerResponse
)

from app.services.assessment_attempt_service import (
    start_assessment,
    submit_answer,
    submit_assessment,
    get_result,
    get_attempt_history
)
from app.schemas.assessment_attempt import (
    StartAssessmentResponse,
    AssessmentResultResponse,
    AssessmentAttemptDetailsResponse
)
from app.services.assessment_attempt_service import (
    start_assessment,
    submit_answer,
    submit_assessment,
    get_result,
    get_attempt_history,
    get_attempt_details
)
router = APIRouter(
    prefix="/assessment-attempts",
    tags=["Assessment Attempts"]
)


@router.post(
    "/start/{assessment_id}",
    response_model=StartAssessmentResponse,
    status_code=status.HTTP_201_CREATED
)
def start(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return start_assessment(
            db,
            assessment_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/{attempt_id}/answer",
    response_model=AssessmentAnswerResponse
)
def answer(
    attempt_id: int,
    answer_data: AssessmentAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return submit_answer(
            db,
            attempt_id,
            answer_data,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.get(
    "/{attempt_id}/details",
    response_model=AssessmentAttemptDetailsResponse
)
def details(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_attempt_details(
            db,
            attempt_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
@router.post("/{attempt_id}/submit")
def submit(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return submit_assessment(
            db,
            attempt_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.get(
    "/{attempt_id}",
    response_model=AssessmentResultResponse
)
def result(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_result(
            db,
            attempt_id,
            current_user
        )

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.get("/history")
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_attempt_history(
        db,
        current_user
    )