"""Tool: add operations (trades) to DLPInvest."""

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


def adicionar_operacoes(
    operacoes: list[dict[str, Any]],
    carteira: str | None = None,
    calc: bool = True,
    return_option: bool = False,
    validar_duplicadas: bool = False,
) -> dict[str, Any]:
    """Adiciona operacoes ao sistema DLPInvest.

    Esta tool posta dados para o endpoint POST /operacoes.

    Args:
        operacoes: Lista de operacoes a serem inseridas (estrutura conforme OperacaoInserirModel).
        carteira: ID da carteira para associar a operaao (query parameter).
        calc: Se deve calcular o resultado (query parameter, default: true).
        return_option: Se deve retornar opcao de retorno (query parameter, default: false).
        validar_duplicadas: Se deve validar duplicatas (query parameter, default: false).

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request(
        "/operacoes",
        method="POST",
        params={
            "carteira": carteira,
            "calc": calc,
            "return_option": return_option,
            "validar_duplicadas": validar_duplicadas,
        },
        json_body=operacoes,
    )
