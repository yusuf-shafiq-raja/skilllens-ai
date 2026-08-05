from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User

from app.schemas.assessment import (
    AssessmentCreate,
    AssessmentUpdate,
    AssessmentResponse,
)

from app.schemas.assessment_question import (
    AssessmentQuestionCreate,
    AssessmentQuestionResponse,
)

from app.services.assessment_service import (
    create_assessment,
    get_all_assessments,
    get_assessment_by_id,
    update_assessment,
    delete_assessment,
)

from app.services.assessment_question_service import (
    add_questions_to_assessment,
    get_assessment_questions,
    remove_question_from_assessment,
)

router = APIRouter(prefix="/assessments", tags=["Assessments"])


# =====================================================
# Assessment CRUD
# =====================================================


@router.post(
    "/", response_model=AssessmentResponse, status_code=status.HTTP_201_CREATED
)
def create_new_assessment(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_assessment(db, assessment, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[AssessmentResponse])
def get_assessments(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_all_assessments(db, current_user)


@router.get("/{assessment_id}", response_model=AssessmentResponse)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    assessment = get_assessment_by_id(db, assessment_id, current_user)

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found."
        )

    return assessment


@router.put("/{assessment_id}", response_model=AssessmentResponse)
def edit_assessment(
    assessment_id: int,
    assessment: AssessmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_assessment(db, assessment_id, assessment, current_user)

    except ValueError as e:

        if str(e) == "Assessment not found.":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{assessment_id}")
def remove_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return delete_assessment(db, assessment_id, current_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# =====================================================
# Assessment Questions
# =====================================================


@router.post(
    "/{assessment_id}/questions", response_model=list[AssessmentQuestionResponse]
)
def add_questions(
    assessment_id: int,
    data: AssessmentQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return add_questions_to_assessment(db, assessment_id, data, current_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/{assessment_id}/questions", response_model=list[AssessmentQuestionResponse]
)
def get_questions(
    assessment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return get_assessment_questions(db, assessment_id, current_user)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{assessment_id}/questions/{question_id}")
def delete_question(
    assessment_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return remove_question_from_assessment(
            db, assessment_id, question_id, current_user
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
