"""Tool: list sub-strategies."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_subestrategias() -> dict[str, Any]:
    """Lista todas as subestrategias de investimento.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request("/subestrategias")
