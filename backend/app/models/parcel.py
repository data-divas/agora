from typing import Optional

from sqlalchemy import JSON, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Parcel(Base, TimestampMixin):
    """Parcel ownership and property information from Regrid API."""

    __tablename__ = "parcels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Link to parking lot
    parking_lot_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("parking_lots.id"), nullable=True, index=True
    )

    # Parcel identification
    apn: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    address: Mapped[str] = mapped_column(Text, nullable=False)
    county: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)

    # Owner information
    owner_name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner_mailing_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    owner_type: Mapped[str] = mapped_column(
        String(50), nullable=False
    )  # individual, llc, corporation, trust, government
    is_likely_commercial: Mapped[bool] = mapped_column(nullable=False, default=False)

    # Property details
    zoning: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    land_use: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    lot_size_sqft: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    assessed_value: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    year_built: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Geometry (GeoJSON polygon)
    geometry: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Rentability analysis
    rentability_score: Mapped[Optional[int]] = mapped_column(
        Integer, nullable=True
    )  # 1-100 score
    rentability_notes: Mapped[Optional[dict]] = mapped_column(
        JSON, nullable=True
    )  # list of strings stored as JSON

    # Relationship to parking lot
    parking_lot: Mapped[Optional["ParkingLot"]] = relationship(
        "ParkingLot", back_populates="parcel"
    )
