from sqlalchemy.orm import Session

from app.models.competency_score import CompetencyScore
from app.models.assessment_attempt import AssessmentAttempt
from app.models.user import User

# ---------------------------------------------------------
# Helper
# ---------------------------------------------------------


def format_scores(scores):

    return [
        {
            "id": score.id,
            "competency_id": score.competency_id,
            "competency_name": score.competency.name,
            "assessment_attempt_id": score.assessment_attempt_id,
            "score": score.score,
            "total_questions": score.total_questions,
            "correct_answers": score.correct_answers,
            "percentage": score.percentage,
            "created_at": score.created_at,
        }
        for score in scores
    ]


# ---------------------------------------------------------
# Get Competency Scores by Attempt
# ---------------------------------------------------------


def get_competency_scores_by_attempt(db: Session, attempt_id: int, current_user: User):

    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == current_user.id,
        )
        .first()
    )

    if not attempt:
        raise ValueError("Assessment attempt not found.")

    scores = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.assessment_attempt_id == attempt.id)
        .all()
    )

    return format_scores(scores)


# ---------------------------------------------------------
# Latest Competency Scores
# ---------------------------------------------------------


def get_latest_competency_scores(db: Session, current_user: User):

    latest_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.is_completed == True,
        )
        .order_by(AssessmentAttempt.submitted_at.desc())
        .first()
    )

    if not latest_attempt:
        return []

    scores = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.assessment_attempt_id == latest_attempt.id)
        .all()
    )

    return format_scores(scores)


# ---------------------------------------------------------
# Competency Score History
# ---------------------------------------------------------


def get_competency_score_history(db: Session, current_user: User):

    scores = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.user_id == current_user.id)
        .order_by(CompetencyScore.created_at.desc())
        .all()
    )

    return format_scores(scores)
