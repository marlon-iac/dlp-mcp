"""Tools: list assets and retrieve details for a single asset."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_ativos() -> dict[str, Any]:
    """Lista todos os ativos disponiveis no sistema.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request("/ativos")


def obter_ativos_detalhes(ticker: str) -> dict[str, Any]:
    """Recupera detalhes de um ativo especifico pelo ticker.

    Args:
        ticker: Ticker do ativo (ex: PETR4).

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request(f"/ativos/{ticker}")
