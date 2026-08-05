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

from app.models.user import User
from app.models.skill import Skill
from app.models.assessment import Assessment

db = SessionLocal()


ASSESSMENTS = [

    {
        "skill": "SQL",
        "title": "SQL Assessment",
        "description": "Evaluate SQL competency.",
        "duration_minutes": 30,
        "passing_score": 12,
        "max_attempts": 3
    },

    {
        "skill": "Python",
        "title": "Python Assessment",
        "description": "Evaluate Python competency.",
        "duration_minutes": 30,
        "passing_score": 12,
        "max_attempts": 3
    },

    {
        "skill": "DBMS",
        "title": "DBMS Assessment",
        "description": "Evaluate DBMS competency.",
        "duration_minutes": 30,
        "passing_score": 12,
        "max_attempts": 3
    }

]


def seed():

    print("\n========== Seeding Assessments ==========\n")

    user = (
        db.query(User)
        .filter(User.email == "yusuf@gmail.com")
        .first()
    )

    if user is None:
        raise Exception("User not found.")

    inserted = 0

    for item in ASSESSMENTS:

        skill = (
            db.query(Skill)
            .filter(Skill.name == item["skill"])
            .first()
        )

        if skill is None:
            print(f"Skill not found : {item['skill']}")
            continue

        exists = (
            db.query(Assessment)
            .filter(
                Assessment.user_id == user.id,
                Assessment.skill_id == skill.id
            )
            .first()
        )

        if exists:
            print(f"Already exists : {item['title']}")
            continue

        assessment = Assessment(

            user_id=user.id,

            skill_id=skill.id,

            title=item["title"],

            description=item["description"],

            duration_minutes=item["duration_minutes"],

            passing_score=item["passing_score"],

            max_attempts=item["max_attempts"],

            is_active=True

        )

        db.add(assessment)

        inserted += 1

        print(f"Inserted : {item['title']}")

    db.commit()

    print("\n==============================")
    print(f"Inserted Assessments : {inserted}")
    print("==============================")

    db.close()


if __name__ == "__main__":
    seed()