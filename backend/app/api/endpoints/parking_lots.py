from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.parking_lot import ParkingLot
from app.schemas.parking_lot import ParkingLotListResponse, ParkingLotResponse

router = APIRouter()


@router.get("/", response_model=List[ParkingLotListResponse])
def list_parking_lots(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    db: Session = Depends(get_db),
) -> List[ParkingLotListResponse]:
    """List all parking lots."""
    parking_lots = (
        db.query(ParkingLot)
        .order_by(ParkingLot.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [ParkingLotListResponse.model_validate(pl) for pl in parking_lots]


@router.get("/{parking_lot_id}", response_model=ParkingLotResponse)
def get_parking_lot(
    parking_lot_id: int,
    db: Session = Depends(get_db),
) -> ParkingLotResponse:
    """Fetch a single parking lot by ID (for drill/detail page)."""
    lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()
    if not lot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Parking lot not found",
        )
    return ParkingLotResponse.model_validate(lot)
