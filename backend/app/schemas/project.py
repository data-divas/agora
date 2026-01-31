from datetime import datetime

from pydantic import BaseModel


class ProjectBase(BaseModel):
    """Base project schema with shared properties."""

    name: str
    required_fund: float | None = None
    project_type: str | None = None
    project_description: str | None = None
    status: str | None = None
    investment_goal: float | None = None


class ProjectCreate(ProjectBase):
    """Schema for creating a new project."""

    pass


class ProjectUpdate(BaseModel):
    """Schema for updating a project. All fields are optional."""

    name: str | None = None
    required_fund: float | None = None
    project_type: str | None = None
    project_description: str | None = None
    status: str | None = None
    investment_goal: float | None = None


class ProjectInDB(ProjectBase):
    """Schema for project as stored in database."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class Project(ProjectBase):
    """Schema for project in API responses."""

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
