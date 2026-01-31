from datetime import datetime
from decimal import Decimal
from enum import Enum as PyEnum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.investment import Investment


class TransactionStatus(PyEnum):
    """Transaction status enum."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class Transaction(Base, TimestampMixin):
    """Transaction model representing a Solana payment event."""

    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        default=uuid4,
        index=True,
    )
    investment_id: Mapped[UUID] = mapped_column(
        ForeignKey("investments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(19, 2),
        nullable=False,
    )
    status: Mapped[TransactionStatus] = mapped_column(
        Enum(TransactionStatus, native_enum=False),
        default=TransactionStatus.PENDING,
        nullable=False,
        index=True,
    )
    solana_transaction_signature: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        unique=True,
        index=True,
    )
    user_wallet: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    pda_address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
        index=True,
    )
    solana_amount: Mapped[Decimal | None] = mapped_column(
        Numeric(19, 9),  # Support up to 9 decimal places for SOL
        nullable=True,
    )
    transaction_verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    verification_attempts: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    failure_reason: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Relationships
    investment: Mapped["Investment"] = relationship(
        "Investment", back_populates="transactions"
    )

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_positive_amount"),
        CheckConstraint(
            "solana_amount IS NULL OR solana_amount > 0",
            name="check_positive_solana_amount",
        ),
    )
