from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.investment import Investment
from app.schemas.investment import InvestmentCreate, InvestmentUpdate


class InvestmentService:
    """Service for investment CRUD operations."""

    @staticmethod
    def get_investment(db: Session, investment_id: UUID) -> Investment | None:
        """Get an investment by ID."""
        return db.query(Investment).filter(Investment.id == investment_id).first()

    @staticmethod
    def get_investments_by_user_id(db: Session, user_id: int) -> List[Investment]:
        """Get all investments for a specific user."""
        return db.query(Investment).filter(Investment.user_id == user_id).all()

    @staticmethod
    def get_investments_by_project_id(db: Session, project_id: str) -> List[Investment]:
        """Get all investments for a specific project."""
        return db.query(Investment).filter(Investment.project_id == project_id).all()

    @staticmethod
    def get_investments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        user_id: int | None = None,
        project_id: str | None = None,
    ) -> List[Investment]:
        """Get a list of investments with optional filtering and pagination."""
        query = db.query(Investment)

        if user_id is not None:
            query = query.filter(Investment.user_id == user_id)
        if project_id is not None:
            query = query.filter(Investment.project_id == project_id)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def create_investment(
        db: Session, investment_create: InvestmentCreate
    ) -> Investment:
        """Create a new investment."""
        db_investment = Investment(
            user_id=investment_create.user_id,
            project_id=investment_create.project_id,
            amount=investment_create.amount,
        )
        db.add(db_investment)
        db.commit()
        db.refresh(db_investment)
        return db_investment

    @staticmethod
    def update_investment(
        db: Session,
        investment_id: UUID,
        investment_update: InvestmentUpdate,
    ) -> Investment | None:
        """Update an investment."""
        db_investment = InvestmentService.get_investment(db, investment_id)
        if not db_investment:
            return None

        update_data = investment_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_investment, field, value)

        db.commit()
        db.refresh(db_investment)
        return db_investment

    @staticmethod
    def delete_investment(db: Session, investment_id: UUID) -> bool:
        """Delete an investment."""
        db_investment = InvestmentService.get_investment(db, investment_id)
        if not db_investment:
            return False

        db.delete(db_investment)
        db.commit()
        return True
