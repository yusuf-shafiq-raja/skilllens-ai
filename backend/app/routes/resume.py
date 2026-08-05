from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.resume import ResumeAnalysisResponse

from app.services.resume_service import analyze_resume

router = APIRouter(prefix="/resume", tags=["Resume Analyzer"])


# ---------------------------------------------------------
# Upload Resume
# ---------------------------------------------------------


@router.post("/upload", response_model=ResumeAnalysisResponse)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:

        return analyze_resume(db=db, file=file)

    except ValueError as e:

        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
