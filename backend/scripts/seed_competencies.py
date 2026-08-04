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
from app.models.competency import Competency

db = SessionLocal()


COMPETENCIES = {

    "SQL": [

        {
            "name": "Query Writing",
            "description": "Write accurate SQL queries."
        },

        {
            "name": "Filtering & Sorting",
            "description": "Use WHERE, ORDER BY and LIMIT effectively."
        },

        {
            "name": "Joins",
            "description": "Combine data from multiple tables."
        },

        {
            "name": "Aggregation",
            "description": "Use GROUP BY and aggregate functions."
        },

        {
            "name": "Subqueries",
            "description": "Solve problems using nested queries."
        }

    ],

    "Python": [

        {
            "name": "Programming Fundamentals",
            "description": "Variables, operators and data types."
        },

        {
            "name": "Functions",
            "description": "Write reusable Python functions."
        },

        {
            "name": "Loops",
            "description": "Solve problems using loops."
        },

        {
            "name": "Object Oriented Programming",
            "description": "Classes, objects and inheritance."
        },

        {
            "name": "Exception Handling",
            "description": "Handle runtime errors."
        }

    ],

    "DBMS": [

        {
            "name": "Database Design",
            "description": "ER diagrams and schema design."
        },

        {
            "name": "Normalization",
            "description": "Apply normal forms."
        },

        {
            "name": "Transactions",
            "description": "Understand ACID properties."
        },

        {
            "name": "Indexing",
            "description": "Improve database performance."
        },

        {
            "name": "Concurrency Control",
            "description": "Manage concurrent transactions."
        }

    ]

}


def seed_competencies():

    print("\n========== Seeding Competencies ==========\n")

    user = (
        db.query(User)
        .filter(User.email == "yusuf@gmail.com")
        .first()
    )

    if user is None:
        raise Exception("User not found.")

    inserted = 0

    skills = db.query(Skill).all()

    for skill in skills:

        if skill.name not in COMPETENCIES:
            continue

        for item in COMPETENCIES[skill.name]:

            existing = (
                db.query(Competency)
                .filter(
                    Competency.skill_id == skill.id,
                    Competency.name == item["name"]
                )
                .first()
            )

            if existing:

                print(f"Already Exists -> {item['name']}")
                continue

            competency = Competency(

                skill_id=skill.id,

                name=item["name"],

                description=item["description"]

            )

            db.add(competency)

            inserted += 1

            print(f"Inserted -> {item['name']}")

    db.commit()

    print("\n==============================")
    print(f"Inserted Competencies : {inserted}")
    print("==============================\n")

    db.close()


if __name__ == "__main__":

    seed_competencies()