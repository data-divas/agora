from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.transaction import Transaction, TransactionConfirm, TransactionCreate
from app.services.transaction import TransactionService

router = APIRouter()


def parse_transaction_id(transaction_id: str) -> UUID:
    """Parse transaction ID with prefix to UUID."""
    prefix = "transaction_"
    if not transaction_id.startswith(prefix):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transaction ID format. Expected format: {prefix}<uuid>",
        )
    uuid_str = transaction_id[len(prefix) :]
    try:
        return UUID(uuid_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid UUID format in transaction ID",
        )


@router.post(
    "/investments/{investment_id}/transactions",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
async def create_transaction(
    investment_id: str,
    transaction_create: TransactionCreate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    """Create a new pending transaction for an investment (Privy JWT required)."""
    # Parse investment_id (with prefix)
    from app.api.endpoints.investments import parse_investment_id
    from app.services.investment import InvestmentService

    inv_uuid = parse_investment_id(investment_id)

    db_investment = InvestmentService.get_investment(db, inv_uuid)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    if db_investment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to create transactions for this investment",
        )

    transaction_create.investment_id = inv_uuid
    db_transaction = TransactionService.create_transaction(db, transaction_create)
    return Transaction.model_validate(db_transaction)


@router.post(
    "/{transaction_id}/confirm",
    response_model=Transaction,
    status_code=status.HTTP_200_OK,
)
async def confirm_transaction(
    transaction_id: str,
    transaction_confirm: TransactionConfirm,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    """Confirm a transaction by verifying it on Solana blockchain (Privy JWT required)."""
    from app.services.investment import InvestmentService

    uuid_id = parse_transaction_id(transaction_id)
    db_transaction = TransactionService.get_transaction(db, uuid_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    db_investment = InvestmentService.get_investment(db, db_transaction.investment_id)
    if not db_investment or db_investment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to confirm this transaction",
        )

    db_transaction = await TransactionService.confirm_transaction(
        db, uuid_id, transaction_confirm
    )
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )
    return Transaction.model_validate(db_transaction)


@router.get("/{transaction_id}", response_model=Transaction)
def get_transaction(
    transaction_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Transaction:
    """Get a transaction by ID (Privy JWT required). You can only view your own transactions."""
    from app.services.investment import InvestmentService

    uuid_id = parse_transaction_id(transaction_id)
    db_transaction = TransactionService.get_transaction(db, uuid_id)
    if not db_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    # Verify transaction belongs to current user
    db_investment = InvestmentService.get_investment(db, db_transaction.investment_id)
    if not db_investment or db_investment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to view this transaction",
        )

    return Transaction.model_validate(db_transaction)


@router.get(
    "/investments/{investment_id}/transactions",
    response_model=List[Transaction],
)
def get_investment_transactions(
    investment_id: str,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[Transaction]:
    """Get all transactions for a specific investment (Privy JWT required)."""
    from app.api.endpoints.investments import parse_investment_id
    from app.services.investment import InvestmentService

    inv_uuid = parse_investment_id(investment_id)

    db_investment = InvestmentService.get_investment(db, inv_uuid)
    if not db_investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found",
        )
    if db_investment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to view transactions for this investment",
        )

    db_transactions = TransactionService.get_transactions_by_investment(db, inv_uuid)
    return [Transaction.model_validate(tx) for tx in db_transactions]


@router.get("/pending", response_model=List[Transaction])
def get_pending_transactions(
    db: Session = Depends(get_db),
) -> List[Transaction]:
    """Get all pending transactions."""
    db_transactions = TransactionService.get_pending_transactions(db)
    return [Transaction.model_validate(tx) for tx in db_transactions]
