from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.concept import (
    ConceptCreate,
    ConceptUpdate,
    ConceptResponse
)
from app.services.concept_service import (
    create_concept,
    get_all_concepts,
    get_concepts_by_skill,
    get_concept_by_id,
    update_concept,
    delete_concept
)

router = APIRouter(
    prefix="/concepts",
    tags=["Concepts"]
)


@router.post(
    "/",
    response_model=ConceptResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_concept(
    concept: ConceptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return create_concept(db, concept, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=list[ConceptResponse]
)
def get_concepts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_concepts(db, current_user)


@router.get(
    "/skill/{skill_id}",
    response_model=list[ConceptResponse]
)
def get_skill_concepts(
    skill_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_concepts_by_skill(
        db,
        skill_id,
        current_user
    )


@router.get(
    "/{concept_id}",
    response_model=ConceptResponse
)
def get_concept(
    concept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    concept = get_concept_by_id(
        db,
        concept_id,
        current_user
    )

    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Concept not found."
        )

    return concept


@router.put(
    "/{concept_id}",
    response_model=ConceptResponse
)
def edit_concept(
    concept_id: int,
    concept: ConceptUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_concept(
            db,
            concept_id,
            concept,
            current_user
        )
    except ValueError as e:
        if str(e) == "Concept not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete(
    "/{concept_id}"
)
def remove_concept(
    concept_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return delete_concept(
            db,
            concept_id,
            current_user
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )