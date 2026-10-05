"""Tool modules for the DLPInvest MCP server.

Each module exposes one tool function decorated with ``@mcp.tool()``.
"""

from dlp_invest_mcp.tools.ativos import obter_ativos, obter_ativos_detalhes
from dlp_invest_mcp.tools.carteira import obter_carteira
from dlp_invest_mcp.tools.corretoras import obter_corretoras
from dlp_invest_mcp.tools.estrategias import obter_estrategias
from dlp_invest_mcp.tools.extrato import obter_extrato
from dlp_invest_mcp.tools.operacoes import obter_operacoes
from dlp_invest_mcp.tools.posicao import obter_posicao
from dlp_invest_mcp.tools.proventos import obter_proventos
from dlp_invest_mcp.tools.rentabilidade import obter_rentabilidade
from dlp_invest_mcp.tools.subestrategias import obter_subestrategias

__all__ = [
    "obter_ativos",
    "obter_ativos_detalhes",
    "obter_carteira",
    "obter_corretoras",
    "obter_estrategias",
    "obter_extrato",
    "obter_operacoes",
    "obter_posicao",
    "obter_proventos",
    "obter_rentabilidade",
    "obter_subestrategias",
]
