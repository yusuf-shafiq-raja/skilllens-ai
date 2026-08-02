from collections import defaultdict

from sqlalchemy.orm import Session

from app.models.question import Question
from app.models.question_competency import QuestionCompetency
from app.models.competency_score import CompetencyScore



# ---------------------------------------------------------
# Calculate Competency Scores
# ---------------------------------------------------------

def calculate_competency_scores(
    db: Session,
    attempt,
    answers
):
    """
    Calculates competency-wise performance for an assessment attempt
    and stores the result in competency_scores table.
    """

    # ----------------------------------------
    # Remove Previous Scores (Safety)
    # ----------------------------------------

    db.query(CompetencyScore).filter(
        CompetencyScore.assessment_attempt_id == attempt.id
    ).delete()

    # ----------------------------------------
    # Dictionary
    # ----------------------------------------

    competency_data = defaultdict(
        lambda: {
            "questions_attempted": 0,
            "correct_answers": 0,
            "earned_weight": 0.0,
            "total_weight": 0.0
        }
    )

    # ----------------------------------------
    # Fetch All Questions Once
    # ----------------------------------------

    question_ids = [
        answer.question_id
        for answer in answers
    ]

    questions = (
        db.query(Question)
        .filter(
            Question.id.in_(question_ids)
        )
        .all()
    )

    question_map = {
        question.id: question
        for question in questions
    }

    # ----------------------------------------
    # Fetch All QuestionCompetencies Once
    # ----------------------------------------

    mappings = (
        db.query(QuestionCompetency)
        .filter(
            QuestionCompetency.question_id.in_(question_ids)
        )
        .all()
    )

    competency_map = defaultdict(list)

    for mapping in mappings:
        competency_map[
            mapping.question_id
        ].append(mapping)

    # ----------------------------------------
    # Process Answers
    # ----------------------------------------

    for answer in answers:

        question = question_map.get(
            answer.question_id
        )

        if question is None:
            continue

        links = competency_map.get(
            question.id,
            []
        )

        for link in links:

            competency = competency_data[
                link.competency_id
            ]

            competency["questions_attempted"] += 1

            competency["total_weight"] += link.weight

            if answer.is_correct:

                competency["correct_answers"] += 1

                competency["earned_weight"] += link.weight

    # ----------------------------------------
    # Save Competency Scores
    # ----------------------------------------

    for competency_id, data in competency_data.items():

        if data["total_weight"] == 0:
            percentage = 0

        else:
            percentage = round(
                (
                    data["earned_weight"]
                    /
                    data["total_weight"]
                ) * 100,
                2
            )
            competency_score = CompetencyScore(

    user_id=attempt.user_id,

    competency_id=competency_id,

    assessment_attempt_id=attempt.id,

    score=round(
        data["earned_weight"],
        2
    ),

    total_questions=data["questions_attempted"],

    correct_answers=data["correct_answers"],

    percentage=percentage
)

        db.add(
            competency_score
        )