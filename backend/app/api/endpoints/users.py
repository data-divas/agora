from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import get_current_user, get_privy_user
from app.auth.privy import PrivyClaims
from app.database import get_db
from app.models.user import User as UserModel
from app.schemas.user import User, UserCreate, UserUpdate
from app.services.user import UserService

router = APIRouter()


@router.get("/me", response_model=User)
def get_current_user_profile(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """Get the authenticated user (Privy JWT required). Links Privy DID to DB user on first request."""
    return current_user


@router.put("/me", response_model=User)
def update_current_user_profile(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Update the authenticated user's profile (email, name)."""
    db_user = UserService.update_user(db, current_user.id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    claims: PrivyClaims = Depends(get_privy_user),
    db: Session = Depends(get_db),
) -> User:
    """Register with Privy: create a user linked to your Privy DID (Privy JWT required). One-time; use PUT /users/me to update profile."""
    if UserService.get_user_by_privy_did(db, claims.user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already registered with Privy. Use GET /users/me to sync or PUT /users/me to update profile.",
        )
    db_user = UserService.create_user_for_privy(db, user_create, claims.user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )
    return db_user


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Get your user by ID (Privy JWT required). You can only read your own profile."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to view another user",
        )
    db_user = UserService.get_user(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.get("/", response_model=List[User])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> List[User]:
    """Get a list of users with pagination (Privy JWT required)."""
    return UserService.get_users(db, skip=skip, limit=limit)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Update a user. You can only update your own profile."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update another user",
        )
    db_user = UserService.update_user(db, user_id, user_update)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Delete a user. You can only delete your own account."""
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete another user",
        )
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
