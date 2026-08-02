from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.assessment import Assessment
from app.models.assessment_attempt import AssessmentAttempt
from app.models.assessment_answer import AssessmentAnswer
from app.models.assessment_question import AssessmentQuestion
from app.models.question import Question
from app.models.user import User
from app.services.competency_service import calculate_competency_scores

# ---------------------------------------------------------
# Start Assessment
# ---------------------------------------------------------

def start_assessment(
    db: Session,
    assessment_id: int,
    current_user: User
):
    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == assessment_id,
            Assessment.user_id == current_user.id
        )
        .first()
    )

    if not assessment:
        raise ValueError("Assessment not found.")

    if not assessment.is_active:
        raise ValueError("Assessment is inactive.")

    links = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == assessment.id
        )
        .all()
    )

    question_ids = [link.question_id for link in links]

    questions = []

    if question_ids:
        questions = (
            db.query(Question)
            .filter(
                Question.id.in_(question_ids)
            )
            .all()
        )

    previous_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id,
            AssessmentAttempt.assessment_id == assessment.id,
            AssessmentAttempt.is_completed == False
        )
        .first()
    )

    # Resume existing attempt
    if previous_attempt:
        return {
            "attempt_id": previous_attempt.id,
            "started_at": previous_attempt.started_at,
            "assessment": assessment,
            "questions": questions
        }

    attempt = AssessmentAttempt(
        user_id=current_user.id,
        assessment_id=assessment.id
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "started_at": attempt.started_at,
        "assessment": assessment,
        "questions": questions
    }

# ---------------------------------------------------------
# Get Assessment Attempt Details
# ---------------------------------------------------------

def get_attempt_details(
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
        raise ValueError("Attempt not found.")

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == attempt.assessment_id
        )
        .first()
    )

    links = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == assessment.id
        )
        .all()
    )

    question_ids = [
        link.question_id
        for link in links
    ]

    questions = []

    if question_ids:

        questions = (
            db.query(Question)
            .filter(
                Question.id.in_(question_ids)
            )
            .all()
        )

    return {

        "attempt_id": attempt.id,

        "started_at": attempt.started_at,

        "assessment": assessment,

        "questions": questions

    }
# ---------------------------------------------------------
# Submit / Update Answer
# ---------------------------------------------------------

def submit_answer(
    db: Session,
    attempt_id: int,
    answer_data,
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
        raise ValueError("Attempt not found.")

    if attempt.is_completed:
        raise ValueError("Assessment already submitted.")

    link = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == attempt.assessment_id,
            AssessmentQuestion.question_id == answer_data.question_id
        )
        .first()
    )

    if not link:
        raise ValueError("Question does not belong to this assessment.")

    question = (
        db.query(Question)
        .filter(
            Question.id == answer_data.question_id
        )
        .first()
    )

    existing = (
        db.query(AssessmentAnswer)
        .filter(
            AssessmentAnswer.attempt_id == attempt.id,
            AssessmentAnswer.question_id == question.id
        )
        .first()
    )

    if existing:
        existing.selected_answer = answer_data.selected_answer.upper()

        db.commit()
        db.refresh(existing)

        return existing

    answer = AssessmentAnswer(
        attempt_id=attempt.id,
        question_id=question.id,
        selected_answer=answer_data.selected_answer.upper()
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer


# ---------------------------------------------------------
# Submit Assessment
# ---------------------------------------------------------

# ---------------------------------------------------------
# Submit Assessment
# ---------------------------------------------------------

def submit_assessment(
    db: Session,
    attempt_id: int,
    current_user: User
):
    # ----------------------------------------
    # Get Attempt
    # ----------------------------------------

    attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.id == attempt_id,
            AssessmentAttempt.user_id == current_user.id
        )
        .first()
    )

    if not attempt:
        raise ValueError("Attempt not found.")

    if attempt.is_completed:
        raise ValueError("Assessment already submitted.")

    # ----------------------------------------
    # Get Submitted Answers
    # ----------------------------------------

    answers = (
        db.query(AssessmentAnswer)
        .filter(
            AssessmentAnswer.attempt_id == attempt.id
        )
        .all()
    )

    if not answers:
        raise ValueError("No answers submitted.")

    # ----------------------------------------
    # Fetch Questions (Single Query)
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
    # Calculate Result
    # ----------------------------------------

    score = 0
    total_marks = 0

    correct_answers = 0
    wrong_answers = 0

    for answer in answers:

        question = question_map.get(
            answer.question_id
        )

        if question is None:
            continue

        total_marks += question.marks

        if (
            answer.selected_answer.upper()
            ==
            question.correct_answer.value.upper()
        ):

            answer.is_correct = True
            answer.marks_obtained = question.marks

            score += question.marks
            correct_answers += 1

        else:

            answer.is_correct = False
            answer.marks_obtained = 0

            wrong_answers += 1

    unanswered_questions = max(
        0,
        len(questions) - len(answers)
    )

    # ----------------------------------------
    # Calculate Percentage
    # ----------------------------------------

    if total_marks > 0:
        percentage = round(
            (score / total_marks) * 100,
            2
        )
    else:
        percentage = 0

    # ----------------------------------------
    # Get Assessment
    # ----------------------------------------

    assessment = (
        db.query(Assessment)
        .filter(
            Assessment.id == attempt.assessment_id
        )
        .first()
    )

    status = (
        "PASSED"
        if percentage >= assessment.passing_score
        else "FAILED"
    )

    # ----------------------------------------
    # Update Attempt
    # ----------------------------------------

    now = datetime.now(timezone.utc)

    attempt.score = score
    attempt.total_marks = total_marks
    attempt.percentage = percentage
    attempt.status = status
    attempt.is_completed = True
    attempt.submitted_at = now
    attempt.time_taken_seconds = int(
        (now - attempt.started_at).total_seconds()
    )

    db.commit()
    db.refresh(attempt)

    # ----------------------------------------
    # Competency Engine (Day 10)
    # ----------------------------------------

    calculate_competency_scores(
    db=db,
    attempt=attempt,
    answers=answers
)

    db.commit()
    # ----------------------------------------
    # Return Result
    # ----------------------------------------

    return {
        "message": "Assessment submitted successfully.",
        "attempt_id": attempt.id,
        "score": score,
        "total_marks": total_marks,
        "percentage": percentage,
        "status": status,
        "correct_answers": correct_answers,
        "wrong_answers": wrong_answers,
        "unanswered_questions": unanswered_questions,
        "time_taken_seconds": attempt.time_taken_seconds
    }
# ---------------------------------------------------------
# Get Result
# ---------------------------------------------------------

def get_result(
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
        raise ValueError("Attempt not found.")

    return attempt


# ---------------------------------------------------------
# Get History
# ---------------------------------------------------------

def get_attempt_history(
    db: Session,
    current_user: User
):
    return (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.user_id == current_user.id
        )
        .order_by(
            AssessmentAttempt.started_at.desc()
        )
        .all()
    )