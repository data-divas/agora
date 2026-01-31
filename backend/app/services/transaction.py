from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionConfirm, TransactionCreate
from app.services.solana import SolanaService


class TransactionService:
    """Service for transaction CRUD operations."""

    @staticmethod
    def get_transaction(db: Session, transaction_id: UUID) -> Transaction | None:
        """Get a transaction by ID."""
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()

    @staticmethod
    def get_transaction_by_signature(db: Session, signature: str) -> Transaction | None:
        """Get a transaction by Solana signature (for idempotency)."""
        return (
            db.query(Transaction)
            .filter(Transaction.solana_transaction_signature == signature)
            .first()
        )

    @staticmethod
    def get_transactions_by_investment(
        db: Session, investment_id: UUID
    ) -> List[Transaction]:
        """Get all transactions for a specific investment."""
        return (
            db.query(Transaction)
            .filter(Transaction.investment_id == investment_id)
            .order_by(Transaction.created_at.desc())
            .all()
        )

    @staticmethod
    def get_pending_transactions(db: Session) -> List[Transaction]:
        """Get all pending transactions."""
        return (
            db.query(Transaction)
            .filter(Transaction.status == TransactionStatus.PENDING)
            .all()
        )

    @staticmethod
    def create_transaction(
        db: Session, transaction_create: TransactionCreate
    ) -> Transaction:
        """Create a new pending transaction."""
        db_transaction = Transaction(
            investment_id=transaction_create.investment_id,
            amount=transaction_create.amount,
            status=TransactionStatus.PENDING,
        )
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    async def confirm_transaction(
        db: Session,
        transaction_id: UUID,
        transaction_confirm: TransactionConfirm,
    ) -> Transaction | None:
        """
        Confirm a transaction by verifying it on Solana blockchain.

        Returns the updated transaction or None if not found.
        """
        db_transaction = TransactionService.get_transaction(db, transaction_id)
        if not db_transaction:
            return None

        # Check if signature already exists (idempotency)
        existing = TransactionService.get_transaction_by_signature(
            db, transaction_confirm.transaction_signature
        )
        if existing and existing.id != transaction_id:
            db_transaction.status = TransactionStatus.FAILED
            db_transaction.failure_reason = "Transaction signature already used"
            db.commit()
            db.refresh(db_transaction)
            return db_transaction

        # Get the project's PDA wallet from the investment
        from app.models.project import Project

        try:
            project_id = int(db_transaction.investment.project_id)
        except (ValueError, TypeError):
            db_transaction.status = TransactionStatus.FAILED
            db_transaction.failure_reason = "Invalid project ID format"
            db.commit()
            db.refresh(db_transaction)
            return db_transaction

        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            db_transaction.status = TransactionStatus.FAILED
            db_transaction.failure_reason = "Project not found"
            db.commit()
            db.refresh(db_transaction)
            return db_transaction

        if not project.solana_pda_wallet:
            db_transaction.status = TransactionStatus.FAILED
            db_transaction.failure_reason = "Project PDA wallet not configured"
            db.commit()
            db.refresh(db_transaction)
            return db_transaction

        # Verify transaction on Solana
        expected_amount = None
        if transaction_confirm.solana_amount:
            from app.services.solana import SolanaService

            expected_amount = SolanaService.convert_sol_to_lamports(
                transaction_confirm.solana_amount
            )

        verification_result = await SolanaService.verify_transaction(
            transaction_confirm.transaction_signature,
            expected_amount=expected_amount,
            expected_recipient=project.solana_pda_wallet,
        )

        db_transaction.verification_attempts += 1
        db_transaction.solana_transaction_signature = (
            transaction_confirm.transaction_signature
        )
        db_transaction.solana_wallet_address = transaction_confirm.wallet_address
        if transaction_confirm.solana_amount:
            db_transaction.solana_amount = transaction_confirm.solana_amount

        if verification_result["verified"]:
            db_transaction.status = TransactionStatus.CONFIRMED
            db_transaction.transaction_verified_at = datetime.utcnow()
        else:
            db_transaction.status = TransactionStatus.FAILED
            db_transaction.failure_reason = verification_result.get(
                "error", "Verification failed"
            )

        db.commit()
        db.refresh(db_transaction)
        return db_transaction

    @staticmethod
    def mark_transaction_failed(
        db: Session, transaction_id: UUID, reason: str
    ) -> Transaction | None:
        """Mark a transaction as failed."""
        db_transaction = TransactionService.get_transaction(db, transaction_id)
        if not db_transaction:
            return None

        db_transaction.status = TransactionStatus.FAILED
        db_transaction.failure_reason = reason
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
