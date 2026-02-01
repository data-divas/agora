from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from app.models.user import User
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Investment(Base, TimestampMixin):
    """Investment model representing a user's position in a project."""

    __tablename__ = "investments"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    project_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="investments")
    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="investment", cascade="all, delete-orphan"
    )

    # Unique constraint: one investment per user-project pair
    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_user_project"),
    )
