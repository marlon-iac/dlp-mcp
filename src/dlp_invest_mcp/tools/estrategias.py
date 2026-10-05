"""Tool: list investment strategies."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_estrategias() -> dict[str, Any]:
    """Lista todas as estrategias de investimento.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request("/estrategias")
