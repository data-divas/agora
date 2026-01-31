from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user schema with shared properties."""

    email: EmailStr
    full_name: str | None = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: str


class UserUpdate(BaseModel):
    """Schema for updating a user. All fields are optional."""

    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    is_active: bool | None = None


class UserInDB(UserBase):
    """Schema for user as stored in database."""

    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class User(UserBase):
    """Schema for user in API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
