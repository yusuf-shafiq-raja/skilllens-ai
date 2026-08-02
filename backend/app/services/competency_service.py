from sqlalchemy.orm import Session

from app.models.competency import Competency
from app.models.skill import Skill
from app.models.user import User

from app.schemas.competency import (
    CompetencyCreate,
    CompetencyUpdate
)


# ---------------------------------------------------------
# Create Competency
# ---------------------------------------------------------

def create_competency(
    db: Session,
    competency: CompetencyCreate,
    current_user: User
):

    skill = (
        db.query(Skill)
        .filter(
            Skill.id == competency.skill_id,
            Skill.user_id == current_user.id
        )
        .first()
    )

    if not skill:
        raise ValueError("Skill not found.")

    existing = (
        db.query(Competency)
        .filter(
            Competency.skill_id == competency.skill_id,
            Competency.name == competency.name
        )
        .first()
    )

    if existing:
        raise ValueError("Competency already exists.")

    new_competency = Competency(
        skill_id=competency.skill_id,
        name=competency.name,
        description=competency.description,
        is_active=competency.is_active
    )

    db.add(new_competency)
    db.commit()
    db.refresh(new_competency)

    return new_competency


# ---------------------------------------------------------
# Get All Competencies
# ---------------------------------------------------------

def get_all_competencies(
    db: Session,
    current_user: User
):

    return (
        db.query(Competency)
        .join(Skill)
        .filter(
            Skill.user_id == current_user.id
        )
        .all()
    )


# ---------------------------------------------------------
# Get Competency By ID
# ---------------------------------------------------------

def get_competency_by_id(
    db: Session,
    competency_id: int,
    current_user: User
):

    return (
        db.query(Competency)
        .join(Skill)
        .filter(
            Competency.id == competency_id,
            Skill.user_id == current_user.id
        )
        .first()
    )


# ---------------------------------------------------------
# Update Competency
# ---------------------------------------------------------

def update_competency(
    db: Session,
    competency_id: int,
    competency: CompetencyUpdate,
    current_user: User
):

    existing = get_competency_by_id(
        db,
        competency_id,
        current_user
    )

    if not existing:
        return None

    update_data = competency.model_dump(
        exclude_unset=True
    )

    if (
        "skill_id" in update_data
        and
        update_data["skill_id"] != existing.skill_id
    ):

        skill = (
            db.query(Skill)
            .filter(
                Skill.id == update_data["skill_id"],
                Skill.user_id == current_user.id
            )
            .first()
        )

        if not skill:
            raise ValueError("Skill not found.")

    for key, value in update_data.items():
        setattr(existing, key, value)

    db.commit()
    db.refresh(existing)

    return existing


# ---------------------------------------------------------
# Delete Competency
# ---------------------------------------------------------

def delete_competency(
    db: Session,
    competency_id: int,
    current_user: User
):

    competency = get_competency_by_id(
        db,
        competency_id,
        current_user
    )

    if not competency:
        return None

    db.delete(competency)
    db.commit()

    return competency