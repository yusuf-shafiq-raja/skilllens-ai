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

from app.models.competency import Competency
from app.models.roadmap import Roadmap

db = SessionLocal()


ROADMAPS = {

    "Query Writing": {
        "title": "Master SQL Query Writing",
        "description": "Build strong SQL query writing skills.",
        "study_topics": "SELECT, FROM, DISTINCT, ORDER BY, LIMIT",
        "practice_tasks": "Solve 30 SELECT problems on HackerRank",
        "next_learning": "Filtering & Sorting"
    },

    "Filtering & Sorting": {
        "title": "Learn WHERE Clause",
        "description": "Master filtering records.",
        "study_topics": "WHERE, LIKE, BETWEEN, IN",
        "practice_tasks": "Solve 25 filtering questions",
        "next_learning": "Joins"
    },

    "Joins": {
        "title": "Master SQL Joins",
        "description": "Understand relationships between tables.",
        "study_topics": "INNER, LEFT, RIGHT, FULL JOIN",
        "practice_tasks": "Practice 20 JOIN queries",
        "next_learning": "Aggregation"
    },

    "Aggregation": {
        "title": "Aggregation Functions",
        "description": "Learn aggregate queries.",
        "study_topics": "COUNT, SUM, AVG, MIN, MAX, GROUP BY",
        "practice_tasks": "Solve aggregation problems",
        "next_learning": "Subqueries"
    },

    "Subqueries": {
        "title": "Subqueries",
        "description": "Nested SQL queries.",
        "study_topics": "Nested SELECT, EXISTS, ANY, ALL",
        "practice_tasks": "Practice 15 subquery problems",
        "next_learning": "Advanced SQL"
    },

    "Programming Fundamentals": {
        "title": "Python Basics",
        "description": "Master variables and data types.",
        "study_topics": "Variables, Data Types, Operators",
        "practice_tasks": "Solve 20 beginner Python problems",
        "next_learning": "Functions"
    },

    "Functions": {
        "title": "Functions in Python",
        "description": "Learn reusable code.",
        "study_topics": "Functions, Parameters, Return",
        "practice_tasks": "Write 15 Python functions",
        "next_learning": "Loops"
    },

    "Loops": {
        "title": "Loops",
        "description": "Practice iteration.",
        "study_topics": "for, while, range",
        "practice_tasks": "Solve looping exercises",
        "next_learning": "Object Oriented Programming"
    },

    "Object Oriented Programming": {
        "title": "Object Oriented Programming",
        "description": "Learn OOP concepts.",
        "study_topics": "Class, Object, Inheritance, Polymorphism",
        "practice_tasks": "Build a Student Management System",
        "next_learning": "Exception Handling"
    },

    "Exception Handling": {
        "title": "Exception Handling",
        "description": "Handle runtime errors.",
        "study_topics": "try, except, finally, raise",
        "practice_tasks": "Practice error handling programs",
        "next_learning": "Advanced Python"
    },

    "Database Design": {
        "title": "ER Modeling",
        "description": "Design relational databases.",
        "study_topics": "Entities, Attributes, Relationships",
        "practice_tasks": "Create 5 ER diagrams",
        "next_learning": "Normalization"
    },

    "Normalization": {
        "title": "Normalization",
        "description": "Reduce redundancy.",
        "study_topics": "1NF, 2NF, 3NF, BCNF",
        "practice_tasks": "Normalize sample tables",
        "next_learning": "Transactions"
    },

    "Transactions": {
        "title": "Transactions",
        "description": "Learn ACID properties.",
        "study_topics": "ACID, COMMIT, ROLLBACK",
        "practice_tasks": "Write transaction queries",
        "next_learning": "Indexing"
    },

    "Indexing": {
        "title": "Indexing",
        "description": "Improve query performance.",
        "study_topics": "Indexes, Clustered, Non-clustered",
        "practice_tasks": "Create indexes on sample tables",
        "next_learning": "Concurrency Control"
    },

    "Concurrency Control": {
        "title": "Concurrency Control",
        "description": "Handle multiple transactions.",
        "study_topics": "Locks, Deadlocks, Serializability",
        "practice_tasks": "Study concurrency scenarios",
        "next_learning": "Advanced DBMS"
    }

}


def seed():

    print("\n========== Seeding Roadmaps ==========\n")

    inserted = 0

    competencies = db.query(Competency).all()

    for competency in competencies:

        data = ROADMAPS.get(competency.name)

        if data is None:
            continue

        exists = db.query(Roadmap).filter(
            Roadmap.competency_id == competency.id
        ).first()

        if exists:
            continue

        db.add(

            Roadmap(

                competency_id=competency.id,

                title=data["title"],

                description=data["description"],

                study_topics=data["study_topics"],

                practice_tasks=data["practice_tasks"],

                next_learning=data["next_learning"],

                is_active=True

            )

        )

        inserted += 1

    db.commit()

    print(f"Inserted : {inserted}")

    db.close()


if __name__ == "__main__":
    seed()