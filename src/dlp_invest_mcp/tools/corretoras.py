"""Tool: list registered brokerages (corretoras)."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_corretoras() -> dict[str, Any]:
    """Lista todas as corretoras cadastradas.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request("/corretoras")
