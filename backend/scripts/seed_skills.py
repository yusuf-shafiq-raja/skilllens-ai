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


db = SessionLocal()


def seed_skills():

    print("\n========== Seeding Skills ==========\n")

    user = (
        db.query(User)
        .filter(User.email == "yusuf@gmail.com")
        .first()
    )

    if user is None:

        raise Exception(
            "User not found. Please register first."
        )

    skills = [

        {
            "name": "SQL",
            "description": "Structured Query Language",
            "category": "Database"
        },

        {
            "name": "Python",
            "description": "Python Programming Language",
            "category": "Programming"
        },

        {
            "name": "DBMS",
            "description": "Database Management System",
            "category": "Database"
        }

    ]

    inserted = 0

    for item in skills:

        existing = (
            db.query(Skill)
            .filter(
                Skill.user_id == user.id,
                Skill.name == item["name"]
            )
            .first()
        )

        if existing:

            print(f"Already Exists -> {item['name']}")
            continue

        skill = Skill(

            user_id=user.id,

            name=item["name"],

            description=item["description"],

            category=item["category"]

        )

        db.add(skill)

        inserted += 1

        print(f"Inserted -> {item['name']}")

    db.commit()

    print("\n==============================")
    print(f"Inserted Skills : {inserted}")
    print("==============================\n")

    db.close()


if __name__ == "__main__":

    seed_skills()