from sqlalchemy.orm import Session

from app.models.roadmap import Roadmap
from app.models.competency import Competency
from app.models.user import User

from app.schemas.roadmap import RoadmapCreate, RoadmapUpdate


def create_roadmap(db: Session, roadmap: RoadmapCreate, current_user: User):

    competency = (
        db.query(Competency).filter(Competency.id == roadmap.competency_id).first()
    )

    if not competency:
        raise ValueError("Competency not found.")

    new_roadmap = Roadmap(**roadmap.model_dump())

    db.add(new_roadmap)

    db.commit()

    db.refresh(new_roadmap)

    return new_roadmap


def get_all_roadmaps(db: Session):

    return db.query(Roadmap).all()


def get_roadmap(db: Session, roadmap_id: int):

    return db.query(Roadmap).filter(Roadmap.id == roadmap_id).first()


def update_roadmap(db: Session, roadmap_id: int, roadmap: RoadmapUpdate):

    existing = get_roadmap(db, roadmap_id)

    if not existing:
        raise ValueError("Roadmap not found.")

    for key, value in roadmap.model_dump(exclude_unset=True).items():

        setattr(existing, key, value)

    db.commit()

    db.refresh(existing)

    return existing


def delete_roadmap(db: Session, roadmap_id: int):

    roadmap = get_roadmap(db, roadmap_id)

    if not roadmap:
        raise ValueError("Roadmap not found.")

    db.delete(roadmap)

    db.commit()

    return {"message": "Roadmap deleted successfully."}
