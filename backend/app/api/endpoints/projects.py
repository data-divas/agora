"""Projects API: get project by parking lot, request project (create pending)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.parking_lot import ParkingLot
from app.models.project import Project as ProjectModel
from app.schemas.project import Project as ProjectSchema
from app.schemas.project import ProjectRequestCreate

router = APIRouter()

PENDING_STATUS = "pending"


@router.get("/by-parking-lot/{parking_lot_id}", response_model=ProjectSchema)
def get_project_by_parking_lot(
    parking_lot_id: int,
    db: Session = Depends(get_db),
) -> ProjectSchema:
    """
    Get the project for a parking lot, if one exists.

    Returns 404 if no project exists for this parking lot.
    """
    project = (
        db.query(ProjectModel)
        .filter(ProjectModel.parking_lot_id == parking_lot_id)
        .first()
    )
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No project for this parking lot",
        )
    return ProjectSchema.model_validate(project)


@router.post("/request", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED)
def request_project(
    body: ProjectRequestCreate,
    db: Session = Depends(get_db),
) -> ProjectSchema:
    """
    Request a project for a parking lot.

    Creates a project with status=pending awaiting approval.
    Returns 400 if a project already exists for this parking lot.
    """
    existing = (
        db.query(ProjectModel)
        .filter(ProjectModel.parking_lot_id == body.parking_lot_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A project already exists for this parking lot",
        )

    parking_lot = (
        db.query(ParkingLot)
        .filter(ParkingLot.id == body.parking_lot_id)
        .first()
    )
    if not parking_lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found",
        )

    project = ProjectModel(
        name=parking_lot.name or f"Project for parking lot {body.parking_lot_id}",
        parking_lot_id=body.parking_lot_id,
        status=PENDING_STATUS,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return ProjectSchema.model_validate(project)
