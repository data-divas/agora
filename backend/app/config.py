from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str = Field(..., description="PostgreSQL database URL")

    # CORS
    allowed_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins",
    )

    # App
    debug: bool = Field(default=False, description="Debug mode")

    # Google Maps (optional; required only for Maps/Places-dependent endpoints)
    google_maps_api_key: str | None = Field(default=None, description="Google Maps API key")

    # Regrid API (for parcel ownership lookup)
    regrid_api_key: str | None = Field(default=None, description="Regrid API key for parcel data")
    regrid_use_sandbox: bool = Field(default=True, description="Use Regrid sandbox environment")

    # Privy (required for server-side JWT verification)
    privy_app_id: str | None = Field(
        default=None, description="Privy app ID from dashboard"
    )
    privy_app_secret: str | None = Field(
        default=None, description="Privy app secret from dashboard"
    )

    # Solana
    solana_rpc_url: str = Field(
        default="https://api.mainnet-beta.solana.com",
        description="Solana RPC endpoint URL",
    )
    solana_network: str = Field(
        default="mainnet",
        description="Solana network (mainnet or devnet)",
    )
    transaction_verification_timeout: int = Field(
        default=300,
        description="Transaction verification timeout in seconds",
    )

    @property
    def origins_list(self) -> List[str]:
        """Parse allowed origins into a list."""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
