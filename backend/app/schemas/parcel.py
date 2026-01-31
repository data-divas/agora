from typing import Optional

from pydantic import BaseModel, Field


class OwnerInfo(BaseModel):
    """Owner information schema."""

    name: str = Field(..., description="Owner name")
    mailing_address: Optional[str] = Field(None, description="Mailing address for owner")
    owner_type: str = Field(
        ..., description="Owner type: individual, llc, corporation, trust, government, unknown"
    )
    is_likely_commercial: bool = Field(
        ..., description="Whether owner appears to be commercial entity"
    )


class ParcelBase(BaseModel):
    """Base parcel information schema."""

    apn: str = Field(..., description="Assessor Parcel Number")
    address: str = Field(..., description="Property address")
    county: str = Field(..., description="County name")
    state: str = Field(..., description="State abbreviation")


class ParcelCreate(ParcelBase):
    """Schema for creating a parcel record."""

    parking_lot_id: Optional[int] = Field(None, description="Associated parking lot ID")
    owner_name: str = Field(..., description="Owner name")
    owner_mailing_address: Optional[str] = Field(None, description="Owner mailing address")
    owner_type: str = Field(..., description="Owner type classification")
    is_likely_commercial: bool = Field(..., description="Whether owner is likely commercial")
    zoning: Optional[str] = Field(None, description="Zoning classification")
    land_use: Optional[str] = Field(None, description="Land use description")
    lot_size_sqft: Optional[float] = Field(None, description="Lot size in square feet")
    assessed_value: Optional[int] = Field(None, description="Assessed property value")
    year_built: Optional[int] = Field(None, description="Year property was built")
    geometry: Optional[dict] = Field(None, description="GeoJSON polygon geometry")
    rentability_score: Optional[int] = Field(None, description="Rentability score (1-100)")
    rentability_notes: Optional[list[str]] = Field(None, description="Rentability analysis notes")


class ParcelInfo(ParcelBase):
    """Detailed parcel information including owner."""

    owner: OwnerInfo = Field(..., description="Owner information")
    zoning: Optional[str] = Field(None, description="Zoning classification")
    land_use: Optional[str] = Field(None, description="Land use description")
    lot_size_sqft: Optional[float] = Field(None, description="Lot size in square feet")
    assessed_value: Optional[int] = Field(None, description="Assessed property value")
    year_built: Optional[int] = Field(None, description="Year property was built")
    geometry: Optional[dict] = Field(None, description="GeoJSON polygon geometry")


class ParcelResponse(ParcelBase):
    """Full parcel response with database fields."""

    id: int
    parking_lot_id: Optional[int] = None
    owner_name: str
    owner_mailing_address: Optional[str] = None
    owner_type: str
    is_likely_commercial: bool
    zoning: Optional[str] = None
    land_use: Optional[str] = None
    lot_size_sqft: Optional[float] = None
    assessed_value: Optional[int] = None
    year_built: Optional[int] = None
    geometry: Optional[dict] = None
    rentability_score: Optional[int] = Field(None, ge=1, le=100)
    rentability_notes: Optional[list[str]] = None

    model_config = {"from_attributes": True}


class ParcelLookupRequest(BaseModel):
    """Request schema for parcel lookup."""

    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")


class ParcelLookupResponse(BaseModel):
    """Response schema for parcel lookup."""

    found: bool = Field(..., description="Whether a parcel was found at the coordinates")
    parcel: Optional[ParcelInfo] = Field(None, description="Parcel information if found")
    rentability_score: Optional[int] = Field(None, ge=1, le=100, description="Rentability score")
    rentability_notes: list[str] = Field(
        default_factory=list, description="Notes about rentability"
    )


class EnrichedParkingLot(BaseModel):
    """Parking lot enriched with parcel data."""

    place_id: str
    name: str
    latitude: float = Field(..., alias="lat")
    longitude: float = Field(..., alias="lng")
    parcel: Optional[ParcelInfo] = None
    rentability_score: Optional[int] = Field(None, ge=1, le=100)
    rentability_notes: list[str] = Field(default_factory=list)

    model_config = {"populate_by_name": True}
