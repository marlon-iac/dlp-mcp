"""MCP server entry point for DLPInvest.

Uses the official ``mcp`` SDK (MCPServer) over stdio.
All tools are registered with ``@server.tool()``.
Logging goes to **stderr**; stdout is reserved for JSON-RPC.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from typing import Any

from mcp.server.mcpserver import MCPServer

from dlp_invest_mcp import __version__
from dlp_invest_mcp.config import settings
from dlp_invest_mcp.tools import (
    adicionar_operacoes as _adicionar_operacoes,
)
from dlp_invest_mcp.tools import (
    obter_ativos as _obter_ativos,
)
from dlp_invest_mcp.tools import (
    obter_ativos_detalhes as _obter_ativos_detalhes,
)
from dlp_invest_mcp.tools import (
    obter_carteira as _obter_carteira,
)
from dlp_invest_mcp.tools import (
    obter_corretoras as _obter_corretoras,
)
from dlp_invest_mcp.tools import (
    obter_estrategias as _obter_estrategias,
)
from dlp_invest_mcp.tools import (
    obter_extrato as _obter_extrato,
)
from dlp_invest_mcp.tools import (
    obter_operacoes as _obter_operacoes,
)
from dlp_invest_mcp.tools import (
    obter_posicao as _obter_posicao,
)
from dlp_invest_mcp.tools import (
    obter_proventos as _obter_proventos,
)
from dlp_invest_mcp.tools import (
    obter_rentabilidade as _obter_rentabilidade,
)
from dlp_invest_mcp.tools import (
    obter_subestrategias as _obter_subestrategias,
)
from dlp_invest_mcp.utils.http import make_request

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
    return _obter_operacoes(
        carteira=carteira,
        status=status,
        data_inicial=data_inicial,
        data_final=data_final,
        limite=limite,
        offset=offset,
    )


@server.tool()
def obter_carteira() -> dict[str, Any]:
    """Recupera a posicao atual dos ativos na carteira.

    ...
    """
    return _obter_carteira()


@server.tool()
def obter_posicao(carteira: str | None = None) -> dict[str, Any]:
    """Recupera a posicao atual dos ativos na carteira.
    ...
    """
    return _obter_posicao(carteira=carteira)


@server.tool()
def obter_rentabilidade(
    carteira: str | None = None,
    data_inicial: str | None = None,
    data_final: str | None = None,
) -> dict[str, Any]:
    """Recupera a rentabilidade da carteira em um periodo.
    ...
    """
    return _obter_rentabilidade(
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
    return _obter_extrato(
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
    return _obter_proventos(
        carteira=carteira,
        data_inicial=data_inicial,
        data_final=data_final,
    )


@server.tool()
def obter_ativos() -> dict[str, Any]:
    """Lista todos os ativos disponiveis no sistema.
    ...
    """
    return _obter_ativos()


@server.tool()
def obter_ativos_detalhes(ticker: str) -> dict[str, Any]:
    """Recupera detalhes de um ativo especifico pelo ticker.
    ...
    """
    return _obter_ativos_detalhes(ticker=ticker)


@server.tool()
def obter_corretoras() -> dict[str, Any]:
    """Lista todas as corretoras cadastradas.
    ...
    """
    return _obter_corretoras()


@server.tool()
def obter_estrategias() -> dict[str, Any]:
    """Lista todas as estrategias de investimento.
    ...
    """
    return _obter_estrategias()


@server.tool()
def obter_subestrategias() -> dict[str, Any]:
    """Lista todas as subestrategias de investimento.
    ...
    """
    return _obter_subestrategias()


if settings.access_mode == "write":

    @server.tool()
    def adicionar_operacoes(
        operacoes: list[dict[str, Any]],
        carteira: str | None = None,
        calc: bool = True,
        return_option: bool = False,
        validar_duplicadas: bool = False,
    ) -> dict[str, Any]:
        """Adiciona operacoes ao sistema DLPInvest."""
        return _adicionar_operacoes(
            operacoes=operacoes,
            carteira=carteira,
            calc=calc,
            return_option=return_option,
            validar_duplicadas=validar_duplicadas,
        )


def _print_help() -> None:
    help_text = """DLP Invest MCP
================================
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
            # Step 1: Check token presence
            if not settings.api_token:
                logger.error(
                    "API token not configured. Please set DLP_INVEST_API_TOKEN environment variable."
                )
                sys.stdout.flush()
                sys.exit(1)
            # Step 2: Check connectivity to the API
            try:
                result = make_request("/api/health")
                if not result.get("success", False):
                    logger.error("Unhealthy API response: %s", result.get("error", "Unknown error"))
                    sys.stdout.flush()
                    sys.exit(2)
            except Exception as exc:
                logger.error("Failed to connect to API: %s", exc)
                sys.stdout.flush()
                sys.exit(2)
            # Step 3: Verify server version compatibility
            logger.info("Doctor check passed: token validated, connectivity confirmed")
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
