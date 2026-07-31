from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.question_competency import (
    QuestionCompetencyCreate,
    QuestionCompetencyUpdate,
    QuestionCompetencyResponse
)

from app.services.question_competency_service import (
    create_question_competency,
    get_all_question_competencies,
    get_question_competency,
    update_question_competency,
    delete_question_competency
)

router = APIRouter(
    prefix="/question-competencies",
    tags=["Question Competencies"]
)


@router.post(
    "/",
    response_model=QuestionCompetencyResponse
)
def create_mapping(
    competency: QuestionCompetencyCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_question_competency(db, competency)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/",
    response_model=list[QuestionCompetencyResponse]
)
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_question_competencies(db)


@router.get(
    "/{mapping_id}",
    response_model=QuestionCompetencyResponse
)
def get_one(
    mapping_id: int,
    db: Session = Depends(get_db)
):
    try:
        return get_question_competency(mapping_id, db)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put(
    "/{mapping_id}",
    response_model=QuestionCompetencyResponse
)
def update_mapping(
    mapping_id: int,
    competency: QuestionCompetencyUpdate,
    db: Session = Depends(get_db)
):
    try:
        return update_question_competency(
            mapping_id,
            competency,
            db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/{mapping_id}"
)
def delete_mapping(
    mapping_id: int,
    db: Session = Depends(get_db)
):
    try:
        return delete_question_competency(
            mapping_id,
            db
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))