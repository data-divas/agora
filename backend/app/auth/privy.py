"""Privy JWT verification and FastAPI dependency."""

from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.services.user import UserService
from app.models.user import User


class PrivyClaims:
    """Verified Privy access token claims (Privy DID and session)."""

    def __init__(self, user_id: str, session_id: str, app_id: str) -> None:
        self.user_id = user_id  # Privy DID
        self.session_id = session_id
        self.app_id = app_id


def _get_privy_client(settings: Settings):
    """Return a PrivyAPI client if credentials are configured."""
    if not settings.privy_app_id or not settings.privy_app_secret:
        return None
    try:
        from privy import PrivyAPI
    except ImportError:
        try:
            from privy_client import PrivyAPI
        except ImportError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Privy SDK not installed",
            ) from None
    return PrivyAPI(
        app_id=settings.privy_app_id,
        app_secret=settings.privy_app_secret,
    )


async def get_privy_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> PrivyClaims:
    """
    FastAPI dependency: verify Authorization Bearer token with Privy and return claims.
    Raises 401 if missing/invalid token or Privy not configured.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    access_token = auth_header.removeprefix("Bearer ").strip()
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    client = _get_privy_client(settings)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Privy server-side auth not configured (PRIVY_APP_ID / PRIVY_APP_SECRET)",
        )

    try:
        verified = client.users.verify_access_token(access_token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        ) from e

    # Map SDK response to our claims (attribute names may vary by SDK version)
    user_id = getattr(verified, "user_id", None) or getattr(verified, "userId", None)
    session_id = getattr(verified, "session_id", None) or getattr(verified, "sessionId", None)
    app_id = getattr(verified, "app_id", None) or getattr(verified, "appId", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )
    return PrivyClaims(
        user_id=str(user_id),
        session_id=str(session_id) if session_id else "",
        app_id=str(app_id) if app_id else "",
    )


async def get_current_user(
    claims: Annotated[PrivyClaims, Depends(get_privy_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    """
    FastAPI dependency: verify Privy token and return the linked DB user.
    Creates a user with placeholder email on first request if none exists for this Privy DID.
    """
    return UserService.get_or_create_user_by_privy(db, claims.user_id)
