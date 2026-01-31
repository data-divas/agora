from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from app.api.v1.router import api_router
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title="Agora API",
    description="FastAPI backend for Agora application",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/api/v1/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def root() -> dict[str, str]:
    """Root endpoint with API documentation links."""
    return {
        "message": "Welcome to Agora API",
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi": "/api/v1/openapi.json",
    }


def custom_openapi():
    """Customize OpenAPI schema for better frontend type generation."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Customize schema as needed for frontend type generation
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
