from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "SkillLens API Running"
    }