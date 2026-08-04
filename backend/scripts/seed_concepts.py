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
from app.models.concept import (
    Concept,
    DifficultyLevel
)

db = SessionLocal()


CONCEPTS = {

    "SQL": [

        {
            "name": "SELECT Statement",
            "description": "Retrieve data from one or more tables.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 2,
            "learning_order": 1
        },

        {
            "name": "WHERE Clause",
            "description": "Filter records using conditions.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 2,
            "learning_order": 2
        },

        {
            "name": "JOINS",
            "description": "Combine rows from multiple tables.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 4,
            "learning_order": 3
        },

        {
            "name": "GROUP BY",
            "description": "Aggregate and group records.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 3,
            "learning_order": 4
        },

        {
            "name": "Subqueries",
            "description": "Nested queries inside SQL statements.",
            "difficulty": DifficultyLevel.HARD,
            "estimated_time": 5,
            "learning_order": 5
        }

    ],

    "Python": [

        {
            "name": "Variables",
            "description": "Store and manage data.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 2,
            "learning_order": 1
        },

        {
            "name": "Functions",
            "description": "Reusable blocks of code.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 3,
            "learning_order": 2
        },

        {
            "name": "Loops",
            "description": "Repeat execution using for and while.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 3,
            "learning_order": 3
        },

        {
            "name": "Object Oriented Programming",
            "description": "Classes and Objects.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 5,
            "learning_order": 4
        },

        {
            "name": "Exception Handling",
            "description": "Handle runtime errors gracefully.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 4,
            "learning_order": 5
        }

    ],

    "DBMS": [

        {
            "name": "ER Model",
            "description": "Entity Relationship Modeling.",
            "difficulty": DifficultyLevel.EASY,
            "estimated_time": 3,
            "learning_order": 1
        },

        {
            "name": "Normalization",
            "description": "Reduce redundancy using normal forms.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 5,
            "learning_order": 2
        },

        {
            "name": "Transactions",
            "description": "ACID properties and transaction management.",
            "difficulty": DifficultyLevel.MEDIUM,
            "estimated_time": 4,
            "learning_order": 3
        },

        {
            "name": "Indexing",
            "description": "Improve query performance.",
            "difficulty": DifficultyLevel.HARD,
            "estimated_time": 4,
            "learning_order": 4
        },

        {
            "name": "Concurrency Control",
            "description": "Handle simultaneous database operations.",
            "difficulty": DifficultyLevel.HARD,
            "estimated_time": 5,
            "learning_order": 5
        }

    ]

}


def seed_concepts():

    print("\n========== Seeding Concepts ==========\n")

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

        if skill.name not in CONCEPTS:
            continue

        for item in CONCEPTS[skill.name]:

            existing = (
                db.query(Concept)
                .filter(
                    Concept.user_id == user.id,
                    Concept.skill_id == skill.id,
                    Concept.name == item["name"]
                )
                .first()
            )

            if existing:
                print(f"Already Exists -> {item['name']}")
                continue

            concept = Concept(

                user_id=user.id,

                skill_id=skill.id,

                name=item["name"],

                description=item["description"],

                difficulty=item["difficulty"],

                estimated_time=item["estimated_time"],

                learning_order=item["learning_order"]

            )

            db.add(concept)

            inserted += 1

            print(f"Inserted -> {item['name']}")

    db.commit()

    print("\n==============================")
    print(f"Inserted Concepts : {inserted}")
    print("==============================")

    db.close()


if __name__ == "__main__":

    seed_concepts()