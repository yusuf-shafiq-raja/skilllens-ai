from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.concept import Concept
from app.models.user import User
from app.schemas.question import QuestionCreate, QuestionUpdate


def create_question(
    db: Session,
    question: QuestionCreate,
    current_user: User
):
    # Verify concept belongs to current user
    concept = (
        db.query(Concept)
        .filter(
            Concept.id == question.concept_id,
            Concept.user_id == current_user.id
        )
        .first()
    )

    if not concept:
        raise ValueError("Concept not found.")

    # Prevent duplicate questions in same concept
    existing_question = (
        db.query(Question)
        .filter(
            Question.user_id == current_user.id,
            Question.concept_id == question.concept_id,
            Question.question == question.question
        )
        .first()
    )

    if existing_question:
        raise ValueError("Question already exists for this concept.")

    new_question = Question(
        user_id=current_user.id,
        concept_id=question.concept_id,
        question=question.question,
        option_a=question.option_a,
        option_b=question.option_b,
        option_c=question.option_c,
        option_d=question.option_d,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        difficulty=question.difficulty,
        question_type=question.question_type,
        marks=question.marks
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question


def get_all_questions(
    db: Session,
    current_user: User
):
    return (
        db.query(Question)
        .filter(
            Question.user_id == current_user.id
        )
        .all()
    )


def get_questions_by_concept(
    db: Session,
    concept_id: int,
    current_user: User
):
    return (
        db.query(Question)
        .filter(
            Question.user_id == current_user.id,
            Question.concept_id == concept_id
        )
        .all()
    )


def get_question_by_id(
    db: Session,
    question_id: int,
    current_user: User
):
    return (
        db.query(Question)
        .filter(
            Question.id == question_id,
            Question.user_id == current_user.id
        )
        .first()
    )


def update_question(
    db: Session,
    question_id: int,
    question: QuestionUpdate,
    current_user: User
):
    existing_question = (
        db.query(Question)
        .filter(
            Question.id == question_id,
            Question.user_id == current_user.id
        )
        .first()
    )

    if not existing_question:
        raise ValueError("Question not found.")

    # Prevent duplicate question text
    if question.question:
        duplicate = (
            db.query(Question)
            .filter(
                Question.user_id == current_user.id,
                Question.concept_id == existing_question.concept_id,
                Question.question == question.question,
                Question.id != question_id
            )
            .first()
        )

        if duplicate:
            raise ValueError("Question already exists for this concept.")

    update_data = question.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(existing_question, key, value)

    db.commit()
    db.refresh(existing_question)

    return existing_question


def delete_question(
    db: Session,
    question_id: int,
    current_user: User
):
    existing_question = (
        db.query(Question)
        .filter(
            Question.id == question_id,
            Question.user_id == current_user.id
        )
        .first()
    )

    if not existing_question:
        raise ValueError("Question not found.")

    db.delete(existing_question)
    db.commit()

    return {
        "message": "Question deleted successfully."
    }