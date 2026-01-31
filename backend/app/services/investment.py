from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.investment import Investment
from app.models.transaction import TransactionStatus
from app.schemas.investment import InvestmentCreate, InvestmentUpdate


class InvestmentService:
    """Service for investment CRUD operations."""

    @staticmethod
    def get_investment(db: Session, investment_id: UUID) -> Investment | None:
        """Get an investment by ID."""
        return db.query(Investment).filter(Investment.id == investment_id).first()

    @staticmethod
    def get_or_create_investment(
        db: Session, user_id: int, project_id: str
    ) -> Investment:
        """Get existing investment or create a new one for user-project pair."""
        investment = (
            db.query(Investment)
            .filter(Investment.user_id == user_id, Investment.project_id == project_id)
            .first()
        )

        if not investment:
            investment = Investment(user_id=user_id, project_id=project_id)
            db.add(investment)
            db.commit()
            db.refresh(investment)

        return investment

    @staticmethod
    def calculate_total_amount(investment: Investment) -> Decimal:
        """Calculate total amount from confirmed transactions."""
        return sum(
            transaction.amount
            for transaction in investment.transactions
            if transaction.status == TransactionStatus.CONFIRMED
        )

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
        return InvestmentService.get_or_create_investment(
            db, investment_create.user_id, investment_create.project_id
        )

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
