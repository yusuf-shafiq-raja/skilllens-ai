from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from app.services.question_service import (
    create_question,
    get_all_questions,
    get_questions_by_concept,
    get_question_by_id,
    update_question,
    delete_question,
)

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_new_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return create_question(db, question, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/", response_model=list[QuestionResponse])
def get_questions(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_all_questions(db, current_user)


@router.get("/concept/{concept_id}", response_model=list[QuestionResponse])
def get_concept_questions(
    concept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_questions_by_concept(db, concept_id, current_user)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = get_question_by_id(db, question_id, current_user)

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found."
        )

    return question


@router.put("/{question_id}", response_model=QuestionResponse)
def edit_question(
    question_id: int,
    question: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return update_question(db, question_id, question, current_user)
    except ValueError as e:
        if str(e) == "Question not found.":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.delete("/{question_id}")
def remove_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        return delete_question(db, question_id, current_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
