from fastapi import APIRouter

from app.api.endpoints import health, investments, parking_lots, transactions, users

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(investments.router, prefix="/investments", tags=["investments"])
api_router.include_router(parking_lots.router, prefix="/parking-lots", tags=["parking-lots"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
