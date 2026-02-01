from decimal import Decimal
from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class TransactionStatus(str, Enum):
    """Transaction status enum."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class TransactionBase(BaseModel):
    """Base transaction schema with shared properties."""

    investment_id: UUID
    amount: Decimal = Field(
        ..., gt=0, description="Transaction amount must be greater than 0"
    )


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction."""

    pass


class TransactionConfirm(BaseModel):
    """Schema for confirming a transaction with Solana details."""

    transaction_signature: str = Field(..., description="Solana transaction signature")
    wallet_address: str = Field(..., description="User's Solana wallet address")
    solana_amount: Decimal | None = Field(
        None, gt=0, description="Amount in SOL (optional, for verification)"
    )


class TransactionInDB(TransactionBase):
    """Schema for transaction as stored in database."""

    id: UUID
    status: TransactionStatus
    solana_transaction_signature: str | None
    user_wallet: str | None
    pda_address: str | None
    solana_amount: Decimal | None
    transaction_verified_at: datetime | None
    verification_attempts: int
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Transaction(TransactionBase):
    """Schema for transaction in API responses with prefixed UUID."""

    id: str = Field(..., description="Transaction ID with prefix")
    status: TransactionStatus
    solana_transaction_signature: str | None
    user_wallet: str | None = Field(None, description="User's Solana wallet address")
    pda_address: str | None = Field(None, description="Project's PDA wallet address")
    solana_amount: Decimal | None
    transaction_verified_at: datetime | None
    verification_attempts: int
    failure_reason: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @model_validator(mode="before")
    @classmethod
    def add_prefix_to_id(cls, data: dict) -> dict:
        """Add prefix to UUID id when creating from ORM object."""
        if isinstance(data, dict) and "id" in data:
            id_value = data["id"]
            if isinstance(id_value, UUID):
                data["id"] = f"transaction_{id_value}"
        return data
