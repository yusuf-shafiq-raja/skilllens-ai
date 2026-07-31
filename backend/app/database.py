from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import DATABASE_URL


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

from app.models.user import User
from app.models.skill import Skill
from app.models.concept import Concept
from app.models.question import Question
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.assessment_attempt import AssessmentAttempt
from app.models.assessment_answer import AssessmentAnswer
from app.models.competency import Competency
from app.models.question_competency import QuestionCompetency
from app.models.competency_score import CompetencyScore


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()