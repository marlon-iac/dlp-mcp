"""Application configuration loaded from environment variables.
Uses pydantic-settings so all settings are validated at startup and
documented in a single place. No required env vars: defaults allow the
server to start and fail gracefully inside tools when the token is missing.
"""

from __future__ import annotations

import os
from typing import Literal

from pydantic import Field, field_validator
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
    # Link mode for uv package installation.
    # Set UV_LINK_MODE=copy in your environment or client config to avoid
    # hardlink failures on Windows/OneDrive/ZFS/bind-mounts.
    # Other valid values: "hardlink" (default), "copy", "symlink".
    # When set to 'copy', uv will copy files instead of creating
    # hardlinks, which avoids errors on Windows/OneDrive/ZFS.
    # Can be configured via:
    #   - Environment variable: UV_LINK_MODE=copy
    #   - Client config (Cursor, Claude, OpenCode): add UV_LINK_MODE to env block
    #   - Shell: Windows: set UV_LINK_MODE=copy (or export on Linux/macOS)
    link_mode: str | None = Field(
        default=None,
        description=(
            "Link mode for uv package installation. "
            "Example values: 'hardlink' (default), 'copy', 'symlink'. "
            "When set to 'copy', uv will copy files instead of creating "
            "hardlinks, which avoids errors on Windows/OneDrive/ZFS. "
            "Configuration methods:\n"
            "  • Environment variable: UV_LINK_MODE=copy\n"
            "  • Client config (Cursor/Claude): add UV_LINK_MODE to env block\n"
            "  • Shell: Windows: set UV_LINK_MODE=copy, Linux/macOS: export UV_LINK_MODE=copy"
        ),
    )
    # Modo de acesso: limita a disponibilidade e a execução de tools mutáveis.
    access_mode: Literal["read", "write"] = Field(
        default="write",
        description=(
            "Modo de acesso ao servidor MCP. "
            "Use 'read' para ocultar tools mutáveis e bloquear escritas. "
            "Use 'write' para habilitar as tools mutáveis implementadas."
        ),
    )

    @field_validator("access_mode", mode="before")
    @classmethod
    def normalize_access_mode(cls, value: object) -> object:
        """Normalize access mode spelling before validating the supported values."""
        return value.strip().lower() if isinstance(value, str) else value


# Module-level settings instance - imported by tools and server
settings = Settings()

# Detect and export UV_LINK_MODE from environment for convenience.
# This handles the case where pydantic-settings doesn't pick up UV_LINK_MODE
# because its prefix (UV_) differs from the configured env_prefix (DLP_INVEST_).
_uv_link_mode = os.environ.get("UV_LINK_MODE")

# Set effective_link_mode: env var takes precedence, then pydantic field, then None
effective_link_mode: str | None = None
if _uv_link_mode is not None:
    effective_link_mode = _uv_link_mode
elif settings.link_mode is not None:
    effective_link_mode = settings.link_mode
