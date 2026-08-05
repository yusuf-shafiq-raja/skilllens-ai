import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.database import SessionLocal

import app.models

from app.models.question import Question
from app.models.concept import Concept
from app.models.competency import Competency
from app.models.question_competency import QuestionCompetency

db = SessionLocal()


CONCEPT_TO_COMPETENCY = {

    # SQL

    "SELECT Statement": "Query Writing",

    "WHERE Clause": "Filtering & Sorting",

    "JOINS": "Joins",

    "GROUP BY": "Aggregation",

    "Subqueries": "Subqueries",

    # Python

    "Variables": "Programming Fundamentals",

    "Functions": "Functions",

    "Loops": "Loops",

    "Object Oriented Programming": "Object Oriented Programming",

    "Exception Handling": "Exception Handling",

    # DBMS

    "ER Model": "Database Design",

    "Normalization": "Normalization",

    "Transactions": "Transactions",

    "Indexing": "Indexing",

    "Concurrency Control": "Concurrency Control"

}


def seed():

    print("\n========== Seeding Question Competencies ==========\n")

    inserted = 0

    questions = db.query(Question).all()

    for question in questions:

        concept = db.query(Concept).filter(
            Concept.id == question.concept_id
        ).first()

        if concept is None:
            continue

        competency_name = CONCEPT_TO_COMPETENCY.get(
            concept.name
        )

        if competency_name is None:
            print(f"No competency mapping for {concept.name}")
            continue

        competency = db.query(Competency).filter(
            Competency.skill_id == concept.skill_id,
            Competency.name == competency_name
        ).first()

        if competency is None:
            print(f"Competency not found : {competency_name}")
            continue

        exists = db.query(QuestionCompetency).filter(
            QuestionCompetency.question_id == question.id,
            QuestionCompetency.competency_id == competency.id
        ).first()

        if exists:
            continue

        db.add(

            QuestionCompetency(

                question_id=question.id,

                competency_id=competency.id,

                weight=1.0

            )

        )

        inserted += 1

    db.commit()

    print(f"\nInserted : {inserted}")

    db.close()


if __name__ == "__main__":
    seed()