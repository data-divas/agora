from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

if TYPE_CHECKING:
    from app.schemas.parcel import ParcelResponse


class PopularTimesData(BaseModel):
    """Schema for popular times data by day of week."""

    monday: Optional[list[int]] = Field(None, description="Hourly utilization 0-100 for Monday")
    tuesday: Optional[list[int]] = Field(None, description="Hourly utilization 0-100 for Tuesday")
    wednesday: Optional[list[int]] = Field(
        None, description="Hourly utilization 0-100 for Wednesday"
    )
    thursday: Optional[list[int]] = Field(
        None, description="Hourly utilization 0-100 for Thursday"
    )
    friday: Optional[list[int]] = Field(None, description="Hourly utilization 0-100 for Friday")
    saturday: Optional[list[int]] = Field(
        None, description="Hourly utilization 0-100 for Saturday"
    )
    sunday: Optional[list[int]] = Field(None, description="Hourly utilization 0-100 for Sunday")


class ParkingLotBase(BaseModel):
    """Base schema for parking lot data."""

    name: str = Field(..., description="Name of the parking lot")
    address: str = Field(..., description="Full address")
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")
    phone_number: Optional[str] = Field(None, description="Contact phone number")
    website: Optional[str] = Field(None, description="Website URL")


class ParkingLotCreate(ParkingLotBase):
    """Schema for creating a new parking lot."""

    place_id: str = Field(..., description="Google Places ID")
    popular_times: Optional[dict] = Field(None, description="Popular times data")
    rating: Optional[float] = Field(None, description="Google rating")
    user_ratings_total: Optional[int] = Field(None, description="Total number of ratings")
    business_status: Optional[str] = Field(None, description="Business operational status")


class ParkingLotUpdate(BaseModel):
    """Schema for updating parking lot information."""

    is_available_for_rent: Optional[bool] = Field(None, description="Available for rent/lease")
    contact_notes: Optional[str] = Field(None, description="Notes about contact attempts")
    estimated_capacity: Optional[int] = Field(None, description="Estimated parking capacity")


class ParkingLotResponse(ParkingLotBase):
    """Schema for parking lot response."""

    id: int
    place_id: str
    popular_times: Optional[dict] = None
    avg_utilization: Optional[float] = Field(
        None, description="Average utilization percentage (0-100)"
    )
    underutilized_hours: Optional[int] = Field(
        None, description="Number of hours per week with < 30% utilization"
    )
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    business_status: Optional[str] = None
    last_synced_at: Optional[datetime] = None
    is_available_for_rent: Optional[bool] = None
    contact_notes: Optional[str] = None
    estimated_capacity: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    # Parcel ownership data (if enriched)
    parcel: Optional["ParcelResponse"] = Field(
        None, description="Parcel ownership and rentability data (if available)"
    )

    model_config = {"from_attributes": True}


class ParkingLotSearchRequest(BaseModel):
    """Schema for parking lot search request."""

    latitude: float = Field(..., description="Search center latitude")
    longitude: float = Field(..., description="Search center longitude")
    radius: int = Field(
        default=5000, ge=100, le=50000, description="Search radius in meters (100-50000)"
    )
    max_results: int = Field(
        default=20, ge=1, le=60, description="Maximum number of results (1-60)"
    )


class ParkingLotSearchResponse(BaseModel):
    """Schema for parking lot search response."""

    total: int = Field(..., description="Total parking lots found")
    parking_lots: list[ParkingLotResponse] = Field(..., description="List of parking lots")
    underutilized_count: int = Field(
        ..., description="Number of underutilized parking lots (avg < 40%)"
    )
