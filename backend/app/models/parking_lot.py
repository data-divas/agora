from datetime import datetime
from typing import Optional

from sqlalchemy import JSON, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class ParkingLot(Base, TimestampMixin):
    """Parking lot model for storing discovered parking lots."""

    __tablename__ = "parking_lots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Google Places data
    place_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(Text, nullable=False)

    # Location
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Contact information
    phone_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Utilization data
    # popular_times format: {day: [hourly utilization 0-100], ...}
    # Example: {"Monday": [10, 15, 20, ...], "Tuesday": [...]}
    popular_times: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    # Calculated metrics
    avg_utilization: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    underutilized_hours: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Additional metadata from Google Places
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    user_ratings_total: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    business_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Data freshness
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Custom fields for manual data entry
    is_available_for_rent: Mapped[Optional[bool]] = mapped_column(nullable=True)
    contact_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    estimated_capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relationship to parcel ownership data
    parcel: Mapped[Optional["Parcel"]] = relationship(
        "Parcel", back_populates="parking_lot", uselist=False
    )
