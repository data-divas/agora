"""Privy JWT verification and FastAPI dependency."""

import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from privy import PrivyAPI
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.database import get_db
from app.models.user import User
from app.services.user import UserService

logger = logging.getLogger(__name__)


class PrivyClaims:
    """Verified Privy access token claims (Privy DID and session)."""

    def __init__(self, user_id: str, session_id: str, app_id: str) -> None:
        self.user_id = user_id  # Privy DID
        self.session_id = session_id
        self.app_id = app_id


def _get_privy_client(settings: Settings) -> PrivyAPI | None:
    """Return a PrivyAPI client if credentials are configured."""
    if not settings.privy_app_id or not settings.privy_app_secret:
        return None
    return PrivyAPI(app_id=settings.privy_app_id, app_secret=settings.privy_app_secret)


async def get_privy_user(
    request: Request,
    settings: Annotated[Settings, Depends(get_settings)],
) -> PrivyClaims:
    """
    FastAPI dependency: verify Authorization Bearer token with Privy and return claims.
    Uses PrivyAPI.users.verify_access_token(access_token).
    Raises 401 if missing/invalid token or Privy not configured.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning("Missing or malformed Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    access_token = auth_header.removeprefix("Bearer ").strip()
    if not access_token:
        logger.warning("Empty access token after parsing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    logger.info(f"Attempting to verify token for request to {request.url.path}")

    client = _get_privy_client(settings)
    if client is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Privy not configured (PRIVY_APP_ID / PRIVY_APP_SECRET)",
        )

    try:
        verified = client.users.verify_access_token(auth_token=access_token)
    except Exception as e:
        logger.error(f"Privy token verification failed: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}",
        ) from e

    # Map SDK response to our claims (SDK may return dict or object)
    def _claim(v, *keys: str):
        for key in keys:
            if isinstance(v, dict):
                val = v.get(key)
            else:
                val = getattr(v, key, None)
            if val is not None:
                return val
        return None

    user_id = _claim(verified, "user_id", "userId")
    session_id = _claim(verified, "session_id", "sessionId")
    app_id = _claim(verified, "app_id", "appId")
    if not user_id:
        logger.error(f"Token verified but missing user_id. Verified object: {verified}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token claims",
        )
    logger.info(f"Successfully verified token for Privy user: {user_id}")
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
