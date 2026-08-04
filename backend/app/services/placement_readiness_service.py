from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.user import User
from app.models.placement_readiness import PlacementReadiness
from app.models.competency_score import CompetencyScore
from app.models.assessment_attempt import AssessmentAttempt


# ---------------------------------------------------------
# Generate Placement Readiness
# ---------------------------------------------------------

def generate_placement_readiness(
    db: Session,
    current_user: User,
    resume_score: float
):

    # ----------------------------------------
    # Latest Assessment
    # ----------------------------------------

    latest_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.is_completed == True
        )
        .order_by(
            AssessmentAttempt.submitted_at.desc()
        )
        .first()
    )

    if latest_attempt:

        assessment_score = latest_attempt.percentage

    else:

        assessment_score = 0


    # ----------------------------------------
    # Average Competency Score
    # ----------------------------------------

    competency_score = (
        db.query(
            func.avg(
                CompetencyScore.percentage
            )
        )
        .filter(
            CompetencyScore.user_id == current_user.id
        )
        .scalar()
    )

    if competency_score is None:

        competency_score = 0


    # ----------------------------------------
    # Overall Score
    # ----------------------------------------

    overall_score = round(

        (
            resume_score +
            assessment_score +
            competency_score
        ) / 3,

        2
    )


    # ----------------------------------------
    # Readiness Level
    # ----------------------------------------

    if overall_score >= 85:

        readiness_level = "Excellent"

        recommendation = (
            "You are highly prepared for placements. "
            "Continue practicing coding and mock interviews."
        )

    elif overall_score >= 70:

        readiness_level = "Placement Ready"

        recommendation = (
            "You are placement ready. "
            "Strengthen weak competencies to improve."
        )

    elif overall_score >= 50:

        readiness_level = "Intermediate"

        recommendation = (
            "Practice assessments regularly and "
            "complete your learning roadmap."
        )

    else:

        readiness_level = "Beginner"

        recommendation = (
            "Focus on learning core concepts before "
            "attempting placements."
        )


    # ----------------------------------------
    # Save / Update
    # ----------------------------------------

    existing = (

        db.query(
            PlacementReadiness
        )

        .filter(
            PlacementReadiness.user_id == current_user.id
        )

        .first()

    )

    if existing:

        existing.resume_score = resume_score

        existing.assessment_score = assessment_score

        existing.competency_score = competency_score

        existing.overall_score = overall_score

        existing.readiness_level = readiness_level

        existing.recommendation = recommendation

        db.commit()

        db.refresh(existing)

        return existing


    placement = PlacementReadiness(

        user_id=current_user.id,

        resume_score=resume_score,

        assessment_score=assessment_score,

        competency_score=competency_score,

        overall_score=overall_score,

        readiness_level=readiness_level,

        recommendation=recommendation

    )

    db.add(placement)

    db.commit()

    db.refresh(placement)

    return placement


# ---------------------------------------------------------
# Get Placement Readiness
# ---------------------------------------------------------

def get_placement_readiness(
    db: Session,
    current_user: User
):

    placement = (

        db.query(
            PlacementReadiness
        )

        .filter(
            PlacementReadiness.user_id == current_user.id
        )

        .first()

    )

    if placement is None:

        raise ValueError(
            "Placement readiness not generated."
        )

    return placement