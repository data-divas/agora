from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with shared properties."""

    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    wallet_address: str | None = None


class UserCreate(UserBase):
    """Schema for creating a new user."""

    pass


class UserUpdate(BaseModel):
    """Schema for updating a user. All fields are optional."""

    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    wallet_address: str | None = None


class UserInDB(UserBase):
    """Schema for user as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class User(UserBase):
    """Schema for user in API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
