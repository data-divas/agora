from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.parking_lot import ParkingLot
from app.schemas.parking_lot import (
    ParkingLotCreate,
    ParkingLotListResponse,
    ParkingLotResponse,
    ParkingLotSearchRequest,
    ParkingLotSearchResponse,
    ParkingLotUpdate,
)
from app.services import google_maps

router = APIRouter()


# ============================================================================
# CRUD Operations
# ============================================================================


@router.get("/", response_model=List[ParkingLotListResponse])
def list_parking_lots(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    underutilized_only: bool = Query(
        False, description="Only return underutilized parking lots (avg < 40%)"
    ),
    db: Session = Depends(get_db),
) -> List[ParkingLotListResponse]:
    """
    List all parking lots from the database.

    Supports pagination and filtering by utilization.
    """
    query = db.query(ParkingLot).order_by(ParkingLot.id)

    if underutilized_only:
        query = query.filter(ParkingLot.avg_utilization < 40)

    parking_lots = query.offset(skip).limit(limit).all()
    return [ParkingLotListResponse.model_validate(pl) for pl in parking_lots]


@router.get("/{parking_lot_id}", response_model=ParkingLotResponse)
def get_parking_lot(
    parking_lot_id: int,
    db: Session = Depends(get_db),
) -> ParkingLotResponse:
    """
    Get a single parking lot by ID.

    Returns detailed information including parcel data if available.
    """
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()

    if not parking_lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    return ParkingLotResponse.model_validate(parking_lot)


@router.post("/", response_model=ParkingLotResponse, status_code=201)
def create_parking_lot(
    parking_lot_data: ParkingLotCreate,
    db: Session = Depends(get_db),
) -> ParkingLotResponse:
    """
    Create a new parking lot manually.

    Requires place_id, name, address, and coordinates.
    """
    # Check if parking lot with this place_id already exists
    existing = db.query(ParkingLot).filter(ParkingLot.place_id == parking_lot_data.place_id).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Parking lot with place_id '{parking_lot_data.place_id}' already exists",
        )

    # Calculate avg utilization and underutilized hours if popular_times provided
    avg_util, underutil_hours = google_maps.calculate_metrics(parking_lot_data.popular_times)

    # Create new parking lot
    parking_lot = ParkingLot(
        place_id=parking_lot_data.place_id,
        name=parking_lot_data.name,
        address=parking_lot_data.address,
        latitude=parking_lot_data.latitude,
        longitude=parking_lot_data.longitude,
        phone_number=parking_lot_data.phone_number,
        website=parking_lot_data.website,
        popular_times=parking_lot_data.popular_times,
        avg_utilization=avg_util,
        underutilized_hours=underutil_hours,
        rating=parking_lot_data.rating,
        user_ratings_total=parking_lot_data.user_ratings_total,
        business_status=parking_lot_data.business_status,
        last_synced_at=datetime.utcnow(),
    )

    db.add(parking_lot)
    db.commit()
    db.refresh(parking_lot)

    return ParkingLotResponse.model_validate(parking_lot)


@router.patch("/{parking_lot_id}", response_model=ParkingLotResponse)
def update_parking_lot(
    parking_lot_id: int,
    update_data: ParkingLotUpdate,
    db: Session = Depends(get_db),
) -> ParkingLotResponse:
    """
    Update parking lot information.

    Allows updating availability, contact notes, and estimated capacity.
    """
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()

    if not parking_lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    # Update fields if provided
    update_dict = update_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(parking_lot, field, value)

    db.commit()
    db.refresh(parking_lot)

    return ParkingLotResponse.model_validate(parking_lot)


@router.delete("/{parking_lot_id}", status_code=204)
def delete_parking_lot(
    parking_lot_id: int,
    db: Session = Depends(get_db),
) -> None:
    """
    Delete a parking lot from the database.
    """
    parking_lot = db.query(ParkingLot).filter(ParkingLot.id == parking_lot_id).first()

    if not parking_lot:
        raise HTTPException(status_code=404, detail="Parking lot not found")

    db.delete(parking_lot)
    db.commit()


# ============================================================================
# Google Maps Search Integration
# ============================================================================


@router.post("/search", response_model=ParkingLotSearchResponse)
def search_and_save_parking_lots(
    search_request: ParkingLotSearchRequest,
    save_to_db: bool = Query(
        True, description="Save discovered parking lots to the database"
    ),
    db: Session = Depends(get_db),
) -> ParkingLotSearchResponse:
    """
    Search for parking lots using Google Maps API and optionally save to database.

    This endpoint:
    1. Searches for parking lots near the specified location
    2. Fetches detailed information including popular times
    3. Calculates utilization metrics
    4. Optionally saves new parking lots to the database (default: True)

    Args:
        search_request: Search parameters (lat, lng, radius, max_results)
        save_to_db: Whether to save discovered parking lots to database
        db: Database session

    Returns:
        List of parking lots with utilization data
    """
    # Fetch parking lots from Google Maps
    places = google_maps.fetch_places_nearby(
        search_request.latitude,
        search_request.longitude,
        search_request.radius,
    )

    # Limit results
    places = places[: search_request.max_results]

    parking_lots: List[ParkingLotResponse] = []
    underutilized_count = 0

    for place in places:
        place_id = place.get("place_id", "")
        name = place.get("name", "Unknown")
        address = place.get("vicinity", "")

        location_data = place.get("geometry", {}).get("location", {})
        latitude = location_data.get("lat", 0)
        longitude = location_data.get("lng", 0)

        rating = place.get("rating")
        user_ratings_total = place.get("user_ratings_total")
        business_status = place.get("business_status")

        # Fetch popular times using populartimes library
        popular_times_data, avg_util = google_maps.fetch_popular_times(place_id)

        # Calculate metrics
        underutil_hours = google_maps.count_underutilized_hours(popular_times_data)

        if avg_util and avg_util < 40:
            underutilized_count += 1

        # Check if parking lot already exists in database
        existing_lot = None
        if save_to_db:
            existing_lot = db.query(ParkingLot).filter(ParkingLot.place_id == place_id).first()

            if existing_lot:
                # Update existing parking lot with fresh data
                existing_lot.name = name
                existing_lot.address = address
                existing_lot.latitude = latitude
                existing_lot.longitude = longitude
                existing_lot.rating = rating
                existing_lot.user_ratings_total = user_ratings_total
                existing_lot.business_status = business_status
                existing_lot.popular_times = popular_times_data
                existing_lot.avg_utilization = avg_util
                existing_lot.underutilized_hours = underutil_hours
                existing_lot.last_synced_at = datetime.utcnow()

                db.commit()
                db.refresh(existing_lot)

                parking_lots.append(ParkingLotResponse.model_validate(existing_lot))
            else:
                # Create new parking lot
                new_lot = ParkingLot(
                    place_id=place_id,
                    name=name,
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    rating=rating,
                    user_ratings_total=user_ratings_total,
                    business_status=business_status,
                    popular_times=popular_times_data,
                    avg_utilization=avg_util,
                    underutilized_hours=underutil_hours,
                    last_synced_at=datetime.utcnow(),
                )

                db.add(new_lot)
                db.commit()
                db.refresh(new_lot)

                parking_lots.append(ParkingLotResponse.model_validate(new_lot))
        else:
            # Just return the data without saving
            # Create a temporary response object
            from pydantic import BaseModel

            class TempResponse(BaseModel):
                id: int = 0
                place_id: str
                name: str
                address: str
                latitude: float
                longitude: float
                phone_number: Optional[str] = None
                website: Optional[str] = None
                popular_times: Optional[dict] = None
                avg_utilization: Optional[float] = None
                underutilized_hours: Optional[int] = None
                rating: Optional[float] = None
                user_ratings_total: Optional[int] = None
                business_status: Optional[str] = None
                last_synced_at: Optional[datetime] = None
                is_available_for_rent: Optional[bool] = None
                contact_notes: Optional[str] = None
                estimated_capacity: Optional[int] = None
                created_at: datetime = datetime.utcnow()
                updated_at: datetime = datetime.utcnow()
                parcel: Optional[dict] = None

            temp_lot = TempResponse(
                place_id=place_id,
                name=name,
                address=address,
                latitude=latitude,
                longitude=longitude,
                popular_times=popular_times_data,
                avg_utilization=avg_util,
                underutilized_hours=underutil_hours,
                rating=rating,
                user_ratings_total=user_ratings_total,
                business_status=business_status,
                last_synced_at=datetime.utcnow(),
            )

            parking_lots.append(ParkingLotResponse.model_validate(temp_lot.model_dump()))

    return ParkingLotSearchResponse(
        total=len(parking_lots),
        parking_lots=parking_lots,
        underutilized_count=underutilized_count,
    )
