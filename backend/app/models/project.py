from sqlalchemy import Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """Project model."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    required_fund: Mapped[float | None] = mapped_column(Float, nullable=True)
    project_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    project_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str | None] = mapped_column(String(255), nullable=True)
