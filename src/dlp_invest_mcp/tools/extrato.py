"""Tool: retrieve the financial statement (extrato)."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_extrato(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    limite: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """Recupera o extrato financeiro da carteira.

    Args:
        carteira: ID ou nome da carteira.
        data_inicial: Data inicial no formato YYYY-MM-DD.
        data_final: Data final no formato YYYY-MM-DD.
        limite: Maximo de resultados.
        offset: Paginacao.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request(
        "/extrato",
        {
            "carteira": carteira,
            "data_inicial": data_inicial,
            "data_final": data_final,
            "limite": limite,
            "offset": offset,
        },
    )
