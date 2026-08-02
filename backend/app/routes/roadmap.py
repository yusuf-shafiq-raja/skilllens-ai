from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user

from app.models.user import User

from app.schemas.roadmap import (
    RoadmapCreate,
    RoadmapUpdate,
    RoadmapResponse
)

from app.services.roadmap_service import (
    create_roadmap,
    get_all_roadmaps,
    get_roadmap,
    update_roadmap,
    delete_roadmap
)

router = APIRouter(
    prefix="/roadmaps",
    tags=["Roadmaps"]
)


# ---------------------------------------------------------
# Create Roadmap
# ---------------------------------------------------------

@router.post(
    "/",
    response_model=RoadmapResponse
)
def add_roadmap(
    roadmap: RoadmapCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:

        return create_roadmap(
            db,
            roadmap,
            current_user
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ---------------------------------------------------------
# Get All Roadmaps
# ---------------------------------------------------------

@router.get(
    "/",
    response_model=list[RoadmapResponse]
)
def read_roadmaps(
    db: Session = Depends(get_db)
):
    return get_all_roadmaps(db)


# ---------------------------------------------------------
# Get Roadmap by ID
# ---------------------------------------------------------

@router.get(
    "/{roadmap_id}",
    response_model=RoadmapResponse
)
def read_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db)
):
    roadmap = get_roadmap(
        db,
        roadmap_id
    )

    if not roadmap:

        raise HTTPException(
            status_code=404,
            detail="Roadmap not found."
        )

    return roadmap


# ---------------------------------------------------------
# Update Roadmap
# ---------------------------------------------------------

@router.put(
    "/{roadmap_id}",
    response_model=RoadmapResponse
)
def edit_roadmap(
    roadmap_id: int,
    roadmap: RoadmapUpdate,
    db: Session = Depends(get_db)
):
    try:

        return update_roadmap(
            db,
            roadmap_id,
            roadmap
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ---------------------------------------------------------
# Delete Roadmap
# ---------------------------------------------------------

@router.delete(
    "/{roadmap_id}"
)
def remove_roadmap(
    roadmap_id: int,
    db: Session = Depends(get_db)
):
    try:

        return delete_roadmap(
            db,
            roadmap_id
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )