from fastapi import FastAPI
from app.routes.health import router as health_router
from app.core.config import APP_NAME, APP_VERSION
app = FastAPI(
    title="SkillLens AI",
    description="AI-Powered Competency Intelligence Platform",
    version="1.0.0"
)

app.include_router(health_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to SkillLens AI 🚀"
    }