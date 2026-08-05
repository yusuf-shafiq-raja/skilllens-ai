from sqlalchemy.orm import Session

from app.models.concept import Concept
from app.models.skill import Skill
from app.models.user import User
from app.schemas.concept import ConceptCreate, ConceptUpdate


def create_concept(db: Session, concept: ConceptCreate, current_user: User):
    # Check whether the skill belongs to the current user
    skill = (
        db.query(Skill)
        .filter(Skill.id == concept.skill_id, Skill.user_id == current_user.id)
        .first()
    )

    if not skill:
        raise ValueError("Skill not found.")

    # Prevent duplicate concept names within the same skill
    existing_concept = (
        db.query(Concept)
        .filter(
            Concept.user_id == current_user.id,
            Concept.skill_id == concept.skill_id,
            Concept.name == concept.name,
        )
        .first()
    )

    if existing_concept:
        raise ValueError("Concept already exists for this skill.")

    new_concept = Concept(
        user_id=current_user.id,
        skill_id=concept.skill_id,
        name=concept.name,
        description=concept.description,
        difficulty=concept.difficulty,
        estimated_time=concept.estimated_time,
        learning_order=concept.learning_order,
    )

    db.add(new_concept)
    db.commit()
    db.refresh(new_concept)

    return new_concept


def get_all_concepts(db: Session, current_user: User):
    return (
        db.query(Concept)
        .filter(Concept.user_id == current_user.id)
        .order_by(Concept.learning_order)
        .all()
    )


def get_concepts_by_skill(db: Session, skill_id: int, current_user: User):
    return (
        db.query(Concept)
        .filter(Concept.user_id == current_user.id, Concept.skill_id == skill_id)
        .order_by(Concept.learning_order)
        .all()
    )


def get_concept_by_id(db: Session, concept_id: int, current_user: User):
    return (
        db.query(Concept)
        .filter(Concept.id == concept_id, Concept.user_id == current_user.id)
        .first()
    )


def update_concept(
    db: Session, concept_id: int, concept: ConceptUpdate, current_user: User
):
    existing_concept = (
        db.query(Concept)
        .filter(Concept.id == concept_id, Concept.user_id == current_user.id)
        .first()
    )

    if not existing_concept:
        raise ValueError("Concept not found.")

    # Prevent duplicate names if updating the name
    if concept.name:
        duplicate = (
            db.query(Concept)
            .filter(
                Concept.user_id == current_user.id,
                Concept.skill_id == existing_concept.skill_id,
                Concept.name == concept.name,
                Concept.id != concept_id,
            )
            .first()
        )

        if duplicate:
            raise ValueError("Concept already exists for this skill.")

    update_data = concept.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_concept, key, value)

    db.commit()
    db.refresh(existing_concept)

    return existing_concept


def delete_concept(db: Session, concept_id: int, current_user: User):
    existing_concept = (
        db.query(Concept)
        .filter(Concept.id == concept_id, Concept.user_id == current_user.id)
        .first()
    )

    if not existing_concept:
        raise ValueError("Concept not found.")

    db.delete(existing_concept)
    db.commit()

    return {"message": "Concept deleted successfully."}
