from typing import List

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Service for user CRUD operations."""

    @staticmethod
    def get_user(db: Session, user_id: int) -> User | None:
        """Get a user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get a user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get a list of users with pagination."""
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def create_user(db: Session, user_create: UserCreate) -> User:
        """Create a new user."""
        hashed_password = hash_password(user_create.password)
        db_user = User(
            email=user_create.email,
            hashed_password=hashed_password,
            full_name=user_create.full_name,
            is_active=user_create.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
        """Update a user."""
        db_user = UserService.get_user(db, user_id)
        if not db_user:
            return None

        update_data = user_update.model_dump(exclude_unset=True)

        # Hash password if it's being updated
        if "password" in update_data:
            update_data["hashed_password"] = hash_password(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete a user."""
        db_user = UserService.get_user(db, user_id)
        if not db_user:
            return False

        db.delete(db_user)
        db.commit()
        return True
