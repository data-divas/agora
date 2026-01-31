from typing import Optional

from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """Project model."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    required_fund: Mapped[float | None] = mapped_column(Float, nullable=True)
    project_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    project_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(String(255), nullable=True)
    investment_goal: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Foreign keys to link projects with parcels and parking lots
    parcel_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("parcels.id"), nullable=True, index=True
    )
    parking_lot_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("parking_lots.id"), nullable=True, index=True
    )

    # Relationships
    parcel: Mapped[Optional["Parcel"]] = relationship("Parcel", lazy="joined")
    parking_lot: Mapped[Optional["ParkingLot"]] = relationship("ParkingLot", lazy="joined")
