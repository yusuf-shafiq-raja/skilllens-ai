from sqlalchemy.orm import Session

from app.models.skill import Skill
from app.schemas.skill import SkillCreate, SkillUpdate


def create_skill(db: Session, skill: SkillCreate):
    db_skill = Skill(
        name=skill.name,
        description=skill.description,
        category=skill.category
    )

    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)

    return db_skill


def get_all_skills(db: Session):
    return db.query(Skill).all()


def get_skill_by_id(db: Session, skill_id: int):
    return db.query(Skill).filter(Skill.id == skill_id).first()


def update_skill(db: Session, skill_id: int, skill: SkillUpdate):
    db_skill = get_skill_by_id(db, skill_id)

    if not db_skill:
        return None

    db_skill.name = skill.name
    db_skill.description = skill.description
    db_skill.category = skill.category

    db.commit()
    db.refresh(db_skill)

    return db_skill


def delete_skill(db: Session, skill_id: int):
    db_skill = get_skill_by_id(db, skill_id)

    if not db_skill:
        return None

    db.delete(db_skill)
    db.commit()

    return db_skill