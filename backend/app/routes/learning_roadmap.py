from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.learning_roadmap import LearningRoadmapResponse

from app.services.roadmap_engine import get_latest_learning_roadmap

router = APIRouter(prefix="/learning-roadmap", tags=["Learning Roadmap"])


@router.get("/latest", response_model=list[LearningRoadmapResponse])
def latest_learning_roadmap(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):

    try:

        return get_latest_learning_roadmap(db, current_user)

    except ValueError as e:

        raise HTTPException(status_code=404, detail=str(e))
