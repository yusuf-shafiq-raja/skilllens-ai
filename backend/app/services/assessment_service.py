from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.skill import Skill
from app.models.user import User
from app.schemas.assessment import AssessmentCreate, AssessmentUpdate


def create_assessment(db: Session, assessment: AssessmentCreate, current_user: User):
    # Verify skill belongs to current user
    skill = (
        db.query(Skill)
        .filter(Skill.id == assessment.skill_id, Skill.user_id == current_user.id)
        .first()
    )

    if not skill:
        raise ValueError("Skill not found.")

    # Prevent duplicate assessment title
    existing_assessment = (
        db.query(Assessment)
        .filter(
            Assessment.user_id == current_user.id, Assessment.title == assessment.title
        )
        .first()
    )

    if existing_assessment:
        raise ValueError("Assessment title already exists.")

    new_assessment = Assessment(
        user_id=current_user.id,
        skill_id=assessment.skill_id,
        title=assessment.title,
        description=assessment.description,
        duration_minutes=assessment.duration_minutes,
        passing_score=assessment.passing_score,
        is_active=assessment.is_active,
    )

    db.add(new_assessment)
    db.commit()
    db.refresh(new_assessment)

    return new_assessment


def get_all_assessments(db: Session, current_user: User):
    return db.query(Assessment).filter(Assessment.user_id == current_user.id).all()


def get_assessment_by_id(db: Session, assessment_id: int, current_user: User):
    return (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )


def update_assessment(
    db: Session, assessment_id: int, assessment: AssessmentUpdate, current_user: User
):
    existing_assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )

    if not existing_assessment:
        raise ValueError("Assessment not found.")

    update_data = assessment.model_dump(exclude_unset=True)

    # Validate skill if changed
    if "skill_id" in update_data:
        skill = (
            db.query(Skill)
            .filter(
                Skill.id == update_data["skill_id"], Skill.user_id == current_user.id
            )
            .first()
        )

        if not skill:
            raise ValueError("Skill not found.")

    # Check duplicate title
    if "title" in update_data:
        duplicate = (
            db.query(Assessment)
            .filter(
                Assessment.user_id == current_user.id,
                Assessment.title == update_data["title"],
                Assessment.id != assessment_id,
            )
            .first()
        )

        if duplicate:
            raise ValueError("Assessment title already exists.")

    for key, value in update_data.items():
        setattr(existing_assessment, key, value)

    db.commit()
    db.refresh(existing_assessment)

    return existing_assessment


def delete_assessment(db: Session, assessment_id: int, current_user: User):
    existing_assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )

    if not existing_assessment:
        raise ValueError("Assessment not found.")

    db.delete(existing_assessment)
    db.commit()

    return {"message": "Assessment deleted successfully."}
