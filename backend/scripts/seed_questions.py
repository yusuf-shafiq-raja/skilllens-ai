import sys
import os
import json

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from app.database import SessionLocal

import app.models

from app.models.user import User
from app.models.skill import Skill
from app.models.concept import Concept
from app.models.question import (
    Question,
    DifficultyLevel,
    QuestionType,
    AnswerOption
)

db = SessionLocal()


DATASET_FOLDER = os.path.join(
    os.path.dirname(__file__),
    "..",
    "datasets"
)


def get_user():

    user = (
        db.query(User)
        .filter(User.email == "yusuf@gmail.com")
        .first()
    )

    if user is None:

        raise Exception(
            "User not found."
        )

    return user


def seed_questions():

    print("\n========== Seeding Questions ==========\n")

    user = get_user()

    inserted = 0

    for file_name in os.listdir(DATASET_FOLDER):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(
            DATASET_FOLDER,
            file_name
        )

        print(f"\nReading {file_name}")

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            questions = json.load(f)

        for item in questions:

            skill = (
                db.query(Skill)
                .filter(
                    Skill.name == item["skill"]
                )
                .first()
            )

            if skill is None:

                print(
                    f"Skill not found : {item['skill']}"
                )

                continue

            concept = (
                db.query(Concept)
                .filter(
                    Concept.skill_id == skill.id,
                    Concept.name == item["concept"]
                )
                .first()
            )

            if concept is None:

                print(
                    f"Concept not found : {item['concept']}"
                )

                continue

            existing = (
                db.query(Question)
                .filter(
                    Question.question == item["question"]
                )
                .first()
            )

            if existing:

                continue

            question = Question(

                user_id=user.id,

                concept_id=concept.id,

                question=item["question"],

                option_a=item["option_a"],

                option_b=item["option_b"],

                option_c=item["option_c"],

                option_d=item["option_d"],

                correct_answer=AnswerOption(
                    item["correct_answer"]
                ),

                explanation=item["explanation"],

                difficulty=DifficultyLevel(
                    item["difficulty"]
                ),

                question_type=QuestionType(
                    item["question_type"]
                ),

                marks=item["marks"]

            )

            db.add(question)

            inserted += 1

    db.commit()

    print("\n============================")
    print(f"Inserted : {inserted}")
    print("============================")

    db.close()


if __name__ == "__main__":

    seed_questions()