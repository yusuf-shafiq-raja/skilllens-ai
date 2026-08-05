from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.question import Question
from app.models.user import User

from app.schemas.assessment_question import AssessmentQuestionCreate


def add_questions_to_assessment(
    db: Session, assessment_id: int, data: AssessmentQuestionCreate, current_user: User
):
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )

    if not assessment:
        raise ValueError("Assessment not found.")

    added_questions = []

    for question_id in data.question_ids:

        question = (
            db.query(Question)
            .filter(Question.id == question_id, Question.user_id == current_user.id)
            .first()
        )

        if not question:
            continue

        exists = (
            db.query(AssessmentQuestion)
            .filter(
                AssessmentQuestion.assessment_id == assessment_id,
                AssessmentQuestion.question_id == question_id,
            )
            .first()
        )

        if exists:
            continue

        link = AssessmentQuestion(
            assessment_id=assessment_id, question_id=question_id, marks=question.marks
        )

        db.add(link)
        added_questions.append(link)

    db.commit()

    return added_questions


def get_assessment_questions(db: Session, assessment_id: int, current_user: User):
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )

    if not assessment:
        raise ValueError("Assessment not found.")

    return (
        db.query(AssessmentQuestion)
        .filter(AssessmentQuestion.assessment_id == assessment_id)
        .all()
    )


def remove_question_from_assessment(
    db: Session, assessment_id: int, question_id: int, current_user: User
):
    assessment = (
        db.query(Assessment)
        .filter(Assessment.id == assessment_id, Assessment.user_id == current_user.id)
        .first()
    )

    if not assessment:
        raise ValueError("Assessment not found.")

    record = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == assessment_id,
            AssessmentQuestion.question_id == question_id,
        )
        .first()
    )

    if not record:
        raise ValueError("Question not found in assessment.")

    db.delete(record)
    db.commit()

    return {"message": "Question removed successfully."}
