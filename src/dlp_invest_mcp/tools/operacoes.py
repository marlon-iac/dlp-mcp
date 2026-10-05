"""Tool: list operations (trades) from DLPInvest."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_operacoes(
    carteira: str | None = None,
    status: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    limite: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """Recupera a lista de operacoes do sistema DLPInvest.

    Args:
        carteira: ID ou nome da carteira para filtrar.
        status: Status da operacao (aberta, fechada, pendente).
        data_inicial: Data inicial no formato YYYY-MM-DD.
        data_final: Data final no formato YYYY-MM-DD.
        limite: Maximo de resultados a retornar.
        offset: Paginacao (quantidade de itens a pular).

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request(
        "/operacoes",
        {
            "carteira": carteira,
            "status": status,
            "data_inicial": data_inicial,
            "data_final": data_final,
            "limite": limite,
            "offset": offset,
        },
    )
