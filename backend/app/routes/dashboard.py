from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.dashboard import DashboardResponse

from app.services.dashboard_service import get_dashboard


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# ---------------------------------------------------------
# Dashboard
# ---------------------------------------------------------

@router.get(
    "",
    response_model=DashboardResponse
)
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:

        return get_dashboard(
            db,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )