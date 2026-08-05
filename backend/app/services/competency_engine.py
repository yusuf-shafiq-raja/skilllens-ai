from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.question_competency import QuestionCompetency
from app.models.competency_score import CompetencyScore


def calculate_competency_scores(db: Session, attempt, answers):

    db.query(CompetencyScore).filter(
        CompetencyScore.assessment_attempt_id == attempt.id
    ).delete()

    competency_data = defaultdict(
        lambda: {"questions": 0, "correct": 0, "earned": 0.0, "total": 0.0}
    )

    question_ids = [answer.question_id for answer in answers]

    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()

    question_map = {q.id: q for q in questions}

    mappings = (
        db.query(QuestionCompetency)
        .filter(QuestionCompetency.question_id.in_(question_ids))
        .all()
    )

    mapping_dict = defaultdict(list)

    for mapping in mappings:

        mapping_dict[mapping.question_id].append(mapping)

    for answer in answers:

        question = question_map.get(answer.question_id)

        if question is None:
            continue

        for mapping in mapping_dict.get(question.id, []):

            competency = competency_data[mapping.competency_id]

            competency["questions"] += 1

            competency["total"] += mapping.weight

            if answer.is_correct:

                competency["correct"] += 1

                competency["earned"] += mapping.weight

    for competency_id, data in competency_data.items():

        percentage = 0

        if data["total"] > 0:

            percentage = round((data["earned"] / data["total"]) * 100, 2)

        db.add(
            CompetencyScore(
                user_id=attempt.user_id,
                competency_id=competency_id,
                assessment_attempt_id=attempt.id,
                score=round(data["earned"], 2),
                total_questions=data["questions"],
                correct_answers=data["correct"],
                percentage=percentage,
            )
        )

    db.commit()
