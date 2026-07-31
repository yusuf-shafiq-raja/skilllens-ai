from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.competency import Competency
from app.models.question_competency import QuestionCompetency

from app.schemas.question_competency import (
    QuestionCompetencyCreate,
    QuestionCompetencyUpdate
)


def create_question_competency(
    db: Session,
    competency_data: QuestionCompetencyCreate
):
    question = db.query(Question).filter(
        Question.id == competency_data.question_id
    ).first()

    if not question:
        raise ValueError("Question not found.")

    competency = db.query(Competency).filter(
        Competency.id == competency_data.competency_id
    ).first()

    if not competency:
        raise ValueError("Competency not found.")

    existing = db.query(QuestionCompetency).filter(
        QuestionCompetency.question_id == competency_data.question_id,
        QuestionCompetency.competency_id == competency_data.competency_id
    ).first()

    if existing:
        raise ValueError("Mapping already exists.")

    mapping = QuestionCompetency(**competency_data.model_dump())

    db.add(mapping)
    db.commit()
    db.refresh(mapping)

    return mapping


def get_all_question_competencies(db: Session):
    return db.query(QuestionCompetency).all()


def get_question_competency(
    mapping_id: int,
    db: Session
):
    mapping = db.query(QuestionCompetency).filter(
        QuestionCompetency.id == mapping_id
    ).first()

    if not mapping:
        raise ValueError("Mapping not found.")

    return mapping


def update_question_competency(
    mapping_id: int,
    competency_data: QuestionCompetencyUpdate,
    db: Session
):
    mapping = db.query(QuestionCompetency).filter(
        QuestionCompetency.id == mapping_id
    ).first()

    if not mapping:
        raise ValueError("Mapping not found.")

    update_data = competency_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(mapping, key, value)

    db.commit()
    db.refresh(mapping)

    return mapping


def delete_question_competency(
    mapping_id: int,
    db: Session
):
    mapping = db.query(QuestionCompetency).filter(
        QuestionCompetency.id == mapping_id
    ).first()

    if not mapping:
        raise ValueError("Mapping not found.")

    db.delete(mapping)
    db.commit()

    return {
        "message": "Question competency mapping deleted successfully."
    }