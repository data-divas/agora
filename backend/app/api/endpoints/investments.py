from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.investment import Investment, InvestmentCreate, InvestmentUpdate
from app.services.investment import InvestmentService

router = APIRouter()


def parse_investment_id(investment_id: str) -> UUID:
    """Parse investment ID with prefix to UUID."""
    prefix = "user_investment_"
    if not investment_id.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid investment ID format. Expected format: {prefix}<uuid>",
        )
    uuid_str = investment_id[len(prefix) :]
    try:
        return UUID(uuid_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format in investment ID",
        )


def _investment_to_response(investment) -> Investment:
    """Convert investment model to response schema with calculated total_amount."""
    total_amount = InvestmentService.calculate_total_amount(investment)
    investment_dict = {
        "id": f"user_investment_{investment.id}",
        "user_id": investment.user_id,
        "project_id": investment.project_id,
        "total_amount": total_amount,
        "created_at": investment.created_at,
        "updated_at": investment.updated_at,
    }
    return Investment.model_validate(investment_dict)


@router.post("/", response_model=Investment, status_code=status.HTTP_201_CREATED)
def create_investment(
    investment_create: InvestmentCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Investment:
    """Create a new investment (or get existing one for user-project pair)."""
    db_investment = InvestmentService.create_investment(db, investment_create)
    return _investment_to_response(db_investment)


@router.get("/{investment_id}", response_model=Investment)
def get_investment(
    investment_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Investment:
    """Get an investment by ID (Privy JWT required). You can only view your own investments."""
    uuid_id = parse_investment_id(investment_id)
    db_investment = InvestmentService.get_investment(db, uuid_id)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    return _investment_to_response(db_investment)


@router.get("/", response_model=List[Investment])
def list_investments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    project_id: str | None = Query(None, description="Filter by project ID"),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Investment]:
    """Get the authenticated user's investments (Privy JWT required)."""
    db_investments = InvestmentService.get_investments(
        db,
        skip=skip,
        limit=limit,
        user_id=current_user.id,
        project_id=project_id,
    )
    return [_investment_to_response(inv) for inv in db_investments]


@router.get("/user/me", response_model=List[Investment])
def get_my_investments(
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Investment]:
    """Get all investments for a specific user."""
    db_investments = InvestmentService.get_investments_by_user_id(db, user_id)
    return [_investment_to_response(inv) for inv in db_investments]


@router.put("/{investment_id}", response_model=Investment)
def update_investment(
    investment_id: str,
    investment_update: InvestmentUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Investment:
    """Update an investment (Privy JWT required). You can only update your own."""
    uuid_id = parse_investment_id(investment_id)
    db_investment = InvestmentService.get_investment(db, uuid_id)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    return _investment_to_response(db_investment)


@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
    investment_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete an investment (Privy JWT required). You can only delete your own."""
    uuid_id = parse_investment_id(investment_id)
    db_investment = InvestmentService.get_investment(db, uuid_id)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    if db_investment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this investment",
        )
    success = InvestmentService.delete_investment(db, uuid_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
