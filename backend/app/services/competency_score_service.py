from sqlalchemy.orm import Session

from app.models.competency_score import CompetencyScore
from app.models.assessment_attempt import AssessmentAttempt
from app.models.user import User


# ---------------------------------------------------------
# Get Competency Scores by Attempt
# ---------------------------------------------------------

def get_competency_scores_by_attempt(
    db: Session,
    attempt_id: int,
    current_user: User
):
    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == current_user.id
        )
        .first()
    )

    if not attempt:
        raise ValueError("Assessment attempt not found.")

    return (
        db.query(CompetencyScore)
        .filter(
            CompetencyScore.assessment_attempt_id == attempt.id
        )
        .all()
    )


# ---------------------------------------------------------
# Get Latest Competency Scores
# ---------------------------------------------------------

def get_latest_competency_scores(
    db: Session,
    current_user: User
):
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

    if not latest_attempt:
        return []

    return (
        db.query(CompetencyScore)
        .filter(
            CompetencyScore.assessment_attempt_id == latest_attempt.id
        )
        .all()
    )


# ---------------------------------------------------------
# Get Competency Score History
# ---------------------------------------------------------

def get_competency_score_history(
    db: Session,
    current_user: User
):
    return (
        db.query(CompetencyScore)
        .filter(
            CompetencyScore.user_id == current_user.id
        )
        .order_by(
            CompetencyScore.created_at.desc()
        )
        .all()
    )