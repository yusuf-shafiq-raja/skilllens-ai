from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import APP_NAME, APP_VERSION
from app.database import Base, engine
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
# Import Models
from app.models.user import User

# Import Routes
from app.routes.health import router as health_router
from app.routes.skill import router as skill_router
from app.routes.concept import router as concept_router
from app.routes.question import router as question_router
from app.routes.assessment import router as assessment_router
from app.routes.assessment_attempt import router as assessment_attempt_router
from app.routes.question_competency import router as question_competency_router
from app.routes.competency import router as competency_router
from app.routes.competency_score import router as competency_score_router
from app.routes.roadmap import router as roadmap_router
from app.routes.resume import router as resume_router
from app.routes.dashboard import router as dashboard_router
from app.models.roadmap import Roadmap
from app.routes.roadmap import router as roadmap_router
from app.routes.learning_roadmap import router as learning_roadmap_router

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI-Powered Competency Intelligence Platform",
    version=APP_VERSION
)
# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(skill_router)
app.include_router(concept_router)
app.include_router(question_router)
app.include_router(assessment_router)
app.include_router(assessment_attempt_router)
app.include_router(question_competency_router)
app.include_router(competency_router)
app.include_router(competency_score_router)
app.include_router(roadmap_router)
app.include_router(resume_router)
app.include_router(dashboard_router)
app.include_router(roadmap_router)
app.include_router(learning_roadmap_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SkillLens AI 🚀"
    }