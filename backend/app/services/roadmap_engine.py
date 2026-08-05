from sqlalchemy.orm import Session

from app.models.assessment_attempt import AssessmentAttempt
from app.models.competency_score import CompetencyScore
from app.models.roadmap import Roadmap
from app.models.competency import Competency
from app.models.user import User


def get_latest_learning_roadmap(db: Session, current_user: User):

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
        raise ValueError("No completed assessment found.")

    competency_scores = (
        db.query(CompetencyScore)
        .filter(CompetencyScore.assessment_attempt_id == latest_attempt.id)
        .all()
    )

    learning_plan = []

    for score in competency_scores:

        roadmap = (
            db.query(Roadmap)
            .filter(
                Roadmap.competency_id == score.competency_id, Roadmap.is_active == True
            )
            .first()
        )

        if roadmap is None:
            continue

        competency = (
            db.query(Competency).filter(Competency.id == score.competency_id).first()
        )

        if score.percentage < 50:

            level = "Weak"

        elif score.percentage < 80:

            level = "Average"

        else:

            level = "Strong"

        learning_plan.append(
            {
                "competency": competency.name,
                "percentage": score.percentage,
                "level": level,
                "study_topics": roadmap.study_topics.split(","),
                "practice_tasks": roadmap.practice_tasks.split(","),
                "next_learning": roadmap.next_learning,
            }
        )

    return learning_plan
