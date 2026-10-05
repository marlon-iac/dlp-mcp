"""Tool: retrieve current asset holdings."""

from __future__ import annotations

from typing import Any

from dlp_invest_mcp.utils.http import make_request


def obter_posicao(carteira: str | None = None) -> dict[str, Any]:
    """Recupera a posicao atual dos ativos na carteira.

    Args:
        carteira: ID ou nome da carteira.

    Returns:
        Dict with ``success`` and either ``data`` or ``error``.
    """
    return make_request("/posicao", {"carteira": carteira})
