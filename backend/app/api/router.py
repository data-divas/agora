from fastapi import APIRouter

from app.api.endpoints import health, investments, users

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])