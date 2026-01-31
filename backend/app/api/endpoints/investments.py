from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
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


@router.post("/", response_model=Investment, status_code=status.HTTP_201_CREATED)
def create_investment(
    investment_create: InvestmentCreate,
    db: Session = Depends(get_db),
) -> Investment:
    """Create a new investment."""
    db_investment = InvestmentService.create_investment(db, investment_create)
    return Investment.model_validate(db_investment)


@router.get("/{investment_id}", response_model=Investment)
def get_investment(
    investment_id: str,
    db: Session = Depends(get_db),
) -> Investment:
    """Get an investment by ID."""
    uuid_id = parse_investment_id(investment_id)
    db_investment = InvestmentService.get_investment(db, uuid_id)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    return Investment.model_validate(db_investment)


@router.get("/", response_model=List[Investment])
def list_investments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    user_id: int | None = Query(None, description="Filter by user ID"),
    project_id: str | None = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db),
) -> List[Investment]:
    """Get a list of investments with optional filtering and pagination."""
    db_investments = InvestmentService.get_investments(
        db, skip=skip, limit=limit, user_id=user_id, project_id=project_id
    )
    return [Investment.model_validate(inv) for inv in db_investments]


@router.get("/user/{user_id}", response_model=List[Investment])
def get_user_investments(
    user_id: int,
    db: Session = Depends(get_db),
) -> List[Investment]:
    """Get all investments for a specific user."""
    db_investments = InvestmentService.get_investments_by_user_id(db, user_id)
    return [Investment.model_validate(inv) for inv in db_investments]


@router.put("/{investment_id}", response_model=Investment)
def update_investment(
    investment_id: str,
    investment_update: InvestmentUpdate,
    db: Session = Depends(get_db),
) -> Investment:
    """Update an investment."""
    uuid_id = parse_investment_id(investment_id)
    db_investment = InvestmentService.update_investment(db, uuid_id, investment_update)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    return Investment.model_validate(db_investment)


@router.delete("/{investment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_investment(
    investment_id: str,
    db: Session = Depends(get_db),
) -> None:
    """Delete an investment."""
    uuid_id = parse_investment_id(investment_id)
    success = InvestmentService.delete_investment(db, uuid_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
