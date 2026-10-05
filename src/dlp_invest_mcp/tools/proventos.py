"""Tool: retrieve dividends and other income (proventos)."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_proventos(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
) -> dict[str, Any]:
    """Recupera os proventos (dividendos, JCP, etc.) recebidos.

    Args:
        carteira: ID ou nome da carteira.
        data_inicial: Data inicial no formato YYYY-MM-DD.
        data_final: Data final no formato YYYY-MM-DD.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request(
        "/proventos",
        {"carteira": carteira, "data_inicial": data_inicial, "data_final": data_final},
    )
