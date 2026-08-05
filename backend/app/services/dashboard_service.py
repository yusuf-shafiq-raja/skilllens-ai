from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.assessment_attempt import AssessmentAttempt
from app.models.competency_score import CompetencyScore
from app.models.competency import Competency

# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------


def get_dashboard(db: Session, current_user: User):

    # ----------------------------------------
    # Total Assessments
    # ----------------------------------------

    total_assessments = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .count()
    )

    # ----------------------------------------
    # Completed Assessments
    # ----------------------------------------

    completed_assessments = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.is_completed == True,
        )
        .count()
    )

    # ----------------------------------------
    # Average Score
    # ----------------------------------------

    average_score = (
        db.query(func.avg(AssessmentAttempt.percentage))
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.is_completed == True,
        )
        .scalar()
    )

    if average_score is None:
        average_score = 0

    average_score = round(average_score, 2)

    # ----------------------------------------
    # Latest Assessment
    # ----------------------------------------

    latest_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.is_completed == True,
        )
        .order_by(AssessmentAttempt.submitted_at.desc())
        .first()
    )

    latest_score = 0

    if latest_attempt:
        latest_score = latest_attempt.percentage

    # ----------------------------------------
    # Top Competency
    # ----------------------------------------

    top_score = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.user_id == current_user.id)
        .order_by(CompetencyScore.percentage.desc())
        .first()
    )

    top_competency = "N/A"

    if top_score:

        competency = (
            db.query(Competency)
            .filter(Competency.id == top_score.competency_id)
            .first()
        )

        if competency:
            top_competency = competency.name

    # ----------------------------------------
    # Weakest Competency
    # ----------------------------------------

    weak_score = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.user_id == current_user.id)
        .order_by(CompetencyScore.percentage.asc())
        .first()
    )

    weakest_competency = "N/A"

    roadmap_priority = "N/A"

    if weak_score:

        competency = (
            db.query(Competency)
            .filter(Competency.id == weak_score.competency_id)
            .first()
        )

        if competency:

            weakest_competency = competency.name

            roadmap_priority = competency.name

    # ----------------------------------------
    # Resume Readiness
    # ----------------------------------------

    resume_readiness = 0.0

    # ----------------------------------------
    # Return
    # ----------------------------------------

    return {
        "user_name": current_user.name,
        "total_assessments": total_assessments,
        "completed_assessments": completed_assessments,
        "average_score": average_score,
        "latest_score": latest_score,
        "top_competency": top_competency,
        "weakest_competency": weakest_competency,
        "roadmap_priority": roadmap_priority,
        "resume_readiness": resume_readiness,
    }
