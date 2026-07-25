from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.skill import SkillCreate, SkillUpdate, SkillResponse
from app.services.skill_service import (
    create_skill,
    get_all_skills,
    get_skill_by_id,
    update_skill,
    delete_skill,
)

router = APIRouter(
    prefix="/skills",
    tags=["Skills"]
)


@router.post("/", response_model=SkillResponse)
def add_skill(skill: SkillCreate, db: Session = Depends(get_db)):
    return create_skill(db, skill)


@router.get("/", response_model=list[SkillResponse])
def read_skills(db: Session = Depends(get_db)):
    return get_all_skills(db)


@router.get("/{skill_id}", response_model=SkillResponse)
def read_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = get_skill_by_id(db, skill_id)

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return skill


@router.put("/{skill_id}", response_model=SkillResponse)
def edit_skill(
    skill_id: int,
    skill: SkillUpdate,
    db: Session = Depends(get_db)
):
    updated_skill = update_skill(db, skill_id, skill)

    if not updated_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return updated_skill


@router.delete("/{skill_id}")
def remove_skill(skill_id: int, db: Session = Depends(get_db)):
    deleted_skill = delete_skill(db, skill_id)

    if not deleted_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    return {
        "message": "Skill deleted successfully"
    }