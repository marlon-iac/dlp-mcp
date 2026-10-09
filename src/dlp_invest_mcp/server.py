"""MCP server entry point for DLPInvest.

Uses the official ``mcp`` SDK (MCPServer) over stdio.
All tools are registered with ``@server.tool()``.
Logging goes to **stderr**; stdout is reserved for JSON-RPC.
"""

from __future__ import annotations

import os
# Força o uv a usar cópias em vez de hardlinks no Windows, evitando o erro de nuvem/partições (os error 396)
os.environ.setdefault("UV_LINK_MODE", "copy")

import asyncio
import logging
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer

from dlp_invest_mcp import __version__
from dlp_invest_mcp.tools import (
    obter_ativos,
    obter_ativos_detalhes,
    obter_carteira,
    obter_corretoras,
    obter_estrategias,
    obter_extrato,
    obter_operacoes,
    obter_posicao,
    obter_proventos,
    obter_rentabilidade,
    obter_subestrategias,
)

# ---------------------------------------------------------------------------
# Logging: stderr only (stdout is the JSON-RPC channel)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP server
# ---------------------------------------------------------------------------
server = MCPServer(
    name="dlp-invest-mcp",
    version=__version__,
    instructions=(
        "Ferramentas para consulta ao sistema financeiro DLPInvest. "
        "Forneeca seu token via variavel de ambiente DLP_INVEST_API_TOKEN."
    ),
)


@server.tool()
def obter_operacoes_tool(
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
    return obter_operacoes(
        carteira=carteira,
        status=status,
        data_inicial=data_inicial,
        data_final=data_final,
        limite=limite,
        offset=offset,
    )


@server.tool()
def obter_carteira_tool() -> dict[str, Any]:
    """Recupera informacoes da carteira do usuario.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_carteira()


@server.tool()
def obter_posicao_tool(carteira: str | None = None) -> dict[str, Any]:
    """Recupera a posicao atual dos ativos na carteira.

    Args:
        carteira: ID ou nome da carteira.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_posicao(carteira=carteira)


@server.tool()
def obter_rentabilidade_tool(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
) -> dict[str, Any]:
    """Recupera a rentabilidade da carteira em um periodo.

    Args:
        carteira: ID ou nome da carteira.
        data_inicial: Data inicial no formato YYYY-MM-DD.
        data_final: Data final no formato YYYY-MM-DD.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_rentabilidade(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
    )


@server.tool()
def obter_extrato_tool(
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
    return obter_extrato(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
        limite=limite,
        offset=offset,
    )


@server.tool()
def obter_proventos_tool(
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
    return obter_proventos(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
    )


@server.tool()
def obter_ativos_tool() -> dict[str, Any]:
    """Lista todos os ativos disponiveis no sistema.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_ativos()


@server.tool()
def obter_ativos_detalhes_tool(ticker: str) -> dict[str, Any]:
    """Recupera detalhes de um ativo especifico pelo ticker.

    Args:
        ticker: Ticker do ativo (ex: PETR4).

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_ativos_detalhes(ticker=ticker)


@server.tool()
def obter_corretoras_tool() -> dict[str, Any]:
    """Lista todas as corretoras cadastradas.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_corretoras()


@server.tool()
def obter_estrategias_tool() -> dict[str, Any]:
    """Lista todas as estrategias de investimento.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_estrategias()


@server.tool()
def obter_subestrategias_tool() -> dict[str, Any]:
    """Lista todas as subestrategias de investimento.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return obter_subestrategias()


def main() -> None:
    """Run the MCP server over stdio.

    This is the entry point used by ``uvx dlp-invest-mcp`` and
    ``python -m dlp_invest_mcp``.
    """
    logger.info("Starting DLPInvest MCP server v%s", __version__)
    asyncio.run(server.run_stdio_async())


if __name__ == "__main__":
    main()

