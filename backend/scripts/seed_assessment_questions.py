import sys
import os
import random

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.database import SessionLocal

import app.models

from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.question import Question
from app.models.concept import Concept
from app.models.skill import Skill

db = SessionLocal()

QUESTIONS_PER_ASSESSMENT = 20


def seed():

    print("\n========== Seeding Assessment Questions ==========\n")

    inserted = 0

    assessments = db.query(Assessment).all()

    for assessment in assessments:

        skill = (
            db.query(Skill)
            .filter(
                Skill.id == assessment.skill_id
            )
            .first()
        )

        if skill is None:
            continue

        questions = (

            db.query(Question)

            .join(
                Concept,
                Question.concept_id == Concept.id
            )

            .filter(
                Concept.skill_id == skill.id
            )

            .all()

        )

        random.shuffle(questions)

        selected = questions[:QUESTIONS_PER_ASSESSMENT]

        count = 0

        for question in selected:

            exists = (

                db.query(AssessmentQuestion)

                .filter(

                    AssessmentQuestion.assessment_id == assessment.id,

                    AssessmentQuestion.question_id == question.id

                )

                .first()

            )

            if exists:
                continue

            db.add(

                AssessmentQuestion(

                    assessment_id=assessment.id,

                    question_id=question.id,

                    marks=question.marks

                )

            )

            inserted += 1

            count += 1

        print(
            f"{assessment.title} -> {count} questions"
        )

    db.commit()

    print("\n==============================")
    print(f"Inserted : {inserted}")
    print("==============================")

    db.close()


if __name__ == "__main__":

    seed()