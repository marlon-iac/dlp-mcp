"""MCP server entry point for DLPInvest.

Uses the official ``mcp`` SDK (MCPServer) over stdio.
All tools are registered with ``@server.tool()``.
Logging goes to **stderr**; stdout is reserved for JSON-RPC.
"""
from __future__ import annotations

import asyncio
import logging
import os
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
def obter_operacoes(
    carteira: str | None = None,
    status: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    limite: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """Recupera a lista de operacoes do sistema DLPInvest.
    ...
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
def obter_carteira() -> dict[str, Any]:
    """Recupera informacoes da carteira do usuario.
    ...
    """
    return obter_carteira()


@server.tool()
def obter_posicao(carteira: str | None = None) -> dict[str, Any]:
    """Recupera a posicao atual dos ativos na carteira.
    ...
    """
    return obter_posicao(carreira=carteira)


@server.tool()
def obter_rentabilidade(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
) -> dict[str, Any]:
    """Recupera a rentabilidade da carteira em um periodo.
    ...
    """
    return obter_rentabilidade(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
    )


@server.tool()
def obter_extrato(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
    limite: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """Recupera o extrato financeiro da carteira.
    ...
    """
    return obter_extrato(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
        limite=limite,
        offset=offset,
    )


@server.tool()
def obter_proventos(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
) -> dict[str, Any]:
    """Recupera os proventos (dividendos, JCP, etc.) recebidos.
    ...
    """
    return obter_proventos(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
    )


@server.tool()
def obter_ativos() -> dict[str, Any]:
    """Lista todos os ativos disponiveis no sistema.
    ...
    """
    return obter_ativos()


@server.tool()
def obter_ativos_detalhes(ticker: str) -> dict[str, Any]:
    """Recupera detalhes de um ativo especifico pelo ticker.
    ...
    """
    return obter_ativos_detalhes(ticker=ticker)


@server.tool()
def obter_corretoras() -> dict[str, Any]:
    """Lista todas as corretoras cadastradas.
    ...
    """
    return obter_corretoras()


@server.tool()
def obter_estrategias() -> dict[str, Any]:
    """Lista todas as estrategias de investimento.
    ...
    """
    return obter_estrategias()


@server.tool()
def obter_subestrategias() -> dict[str, Any]:
    """Lista todas as subestrategias de investimento.
    ...
    """
    return obter_subestrategias()


def _print_help() -> None:
    help_text = """DLP Invest MCP
==============
Instalação rápida:
  uvx dlp-invest-mcp

Configuração do MCP:
  Veja README.md para exemplos em Cursor, Gemini e OpenCode.

Doctor:
  dlp-invest-mcp doctor

Ajuda geral:
  dlp-invest-mcp --help
"""
    sys.stdout.write(help_text)
    sys.stdout.flush()


def main() -> None:
    """Run the MCP server over stdio.

    This is the entry point used by ``uvx dlp-invest-mcp`` and
    ``python -m dlp_invest_mcp``.
    """
    # Process special args FIRST, before anything else
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg in ("--help", "-h"):
            _print_help()
            sys.exit(0)
        elif arg == "doctor":
            logger.info("Doctor check not implemented yet.")
            sys.stdout.flush()
            sys.exit(0)

    logger.info("Starting DLPInvest MCP server v%s", __version__)
    try:
        asyncio.run(server.run_stdio_async())
    except KeyboardInterrupt:
        logger.info("Servidor interrompido pelo usuário. Encerrando...")
        sys.stdout.flush()
        sys.stderr.flush()


if __name__ == "__main__":
    main()