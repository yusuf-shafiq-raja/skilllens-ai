from fastapi import FastAPI

from app.core.config import APP_NAME, APP_VERSION
from app.database import Base, engine

# Import Models
from app.models.user import User

# Import Routes
from app.routes.health import router as health_router

# Create Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI-Powered Competency Intelligence Platform",
    version=APP_VERSION
)

# Register Routes
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SkillLens AI 🚀"
    }