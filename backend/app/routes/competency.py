from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies import get_current_user
from app.database import get_db

from app.models.user import User

from app.schemas.competency import (
    CompetencyCreate,
    CompetencyUpdate,
    CompetencyResponse,
)

from app.services.competency_service import (
    create_competency,
    get_all_competencies,
    get_competency_by_id,
    update_competency,
    delete_competency,
)

router = APIRouter(prefix="/competencies", tags=["Competencies"])


@router.post("/", response_model=CompetencyResponse)
def add_competency(
    competency: CompetencyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_competency(db, competency, current_user)


@router.get("/", response_model=list[CompetencyResponse])
def read_competencies(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    return get_all_competencies(db, current_user)


@router.get("/{competency_id}", response_model=CompetencyResponse)
def read_competency(
    competency_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    competency = get_competency_by_id(db, competency_id, current_user)

    if not competency:
        raise HTTPException(status_code=404, detail="Competency not found")

    return competency


@router.put("/{competency_id}", response_model=CompetencyResponse)
def edit_competency(
    competency_id: int,
    competency: CompetencyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    updated_competency = update_competency(db, competency_id, competency, current_user)

    if not updated_competency:
        raise HTTPException(status_code=404, detail="Competency not found")

    return updated_competency


@router.delete("/{competency_id}")
def remove_competency(
    competency_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deleted_competency = delete_competency(db, competency_id, current_user)

    if not deleted_competency:
        raise HTTPException(status_code=404, detail="Competency not found")

    return {"message": "Competency deleted successfully"}
