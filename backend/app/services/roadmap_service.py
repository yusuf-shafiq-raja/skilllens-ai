from sqlalchemy.orm import Session

from app.models.competency_score import CompetencyScore
from app.models.competency import Competency
from app.models.concept import Concept
from app.models.assessment_attempt import AssessmentAttempt
from app.models.user import User


# ---------------------------------------------------------
# Estimated Learning Hours
# ---------------------------------------------------------

def estimate_learning_hours(percentage: float) -> int:

    if percentage >= 90:
        return 1

    elif percentage >= 70:
        return 3

    elif percentage >= 40:
        return 6

    return 10


# ---------------------------------------------------------
# Latest Roadmap
# ---------------------------------------------------------

def get_latest_roadmap(
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

    if latest_attempt is None:
        raise ValueError(
            "No completed assessment found."
        )

    return get_roadmap_by_attempt(
        db,
        latest_attempt.id,
        current_user
    )


# ---------------------------------------------------------
# Roadmap By Attempt
# ---------------------------------------------------------

def get_roadmap_by_attempt(
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

    if attempt is None:
        raise ValueError(
            "Assessment attempt not found."
        )

    scores = (
        db.query(CompetencyScore)
        .filter(
            CompetencyScore.assessment_attempt_id == attempt.id
        )
        .order_by(
            CompetencyScore.percentage.asc()
        )
        .all()
    )

    roadmap = []

    priority = 1

    for score in scores:

        competency = (
            db.query(Competency)
            .filter(
                Competency.id == score.competency_id
            )
            .first()
        )

        if competency is None:
            continue

        concepts = (
            db.query(Concept)
            .filter(
                Concept.skill_id == competency.skill_id
            )
            .order_by(
                Concept.learning_order.asc()
            )
            .all()
        )

        roadmap.append(

            {
                "competency": competency.name,

                "current_level": score.level,

                "percentage": score.percentage,

                "priority": priority,

                "estimated_hours": estimate_learning_hours(
                    score.percentage
                ),

                "recommended_concepts": [
                    concept.name
                    for concept in concepts
                ]
            }

        )

        priority += 1

    return {
        "roadmap": roadmap
    }