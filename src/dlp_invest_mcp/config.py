"""Application configuration loaded from environment variables.

Uses pydantic-settings so all settings are validated at startup and
documented in a single place. No required env vars: defaults allow the
server to start and fail gracefully inside tools when the token is missing.
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the DLPInvest MCP server."""

    model_config = SettingsConfigDict(
        env_prefix="DLP_INVEST_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    api_base_url: str = Field(
        default="https://users.dlpinvest.com.br",
        description="Base URL of the DLPInvest REST API.",
    )
    api_token: str = Field(
        default="",
        description="DLPInvest API token (Bearer). Leave empty to disable requests.",
    )
    request_timeout_seconds: float = Field(
        default=30.0,
        description="HTTP request timeout in seconds.",
        gt=0,
    )


settings = Settings()
"""Singleton settings instance imported by tools and server."""
