from decimal import Decimal
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class InvestmentBase(BaseModel):
    """Base investment schema with shared properties."""

    user_id: int
    project_id: str
    amount: Decimal = Field(..., gt=0, description="Investment amount must be greater than 0")


class InvestmentCreate(InvestmentBase):
    """Schema for creating a new investment."""

    pass


class InvestmentUpdate(BaseModel):
    """Schema for updating an investment. All fields are optional."""

    project_id: str | None = None
    amount: Decimal | None = Field(None, gt=0, description="Investment amount must be greater than 0")


class InvestmentInDB(InvestmentBase):
    """Schema for investment as stored in database."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Investment(InvestmentBase):
    """Schema for investment in API responses with prefixed UUID."""

    id: str = Field(..., description="Investment ID with prefix")
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
                data["id"] = f"user_investment_{id_value}"
        return data
