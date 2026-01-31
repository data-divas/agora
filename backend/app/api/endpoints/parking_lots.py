from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.parking_lot import ParkingLot
from app.schemas.parking_lot import ParkingLotListResponse

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
