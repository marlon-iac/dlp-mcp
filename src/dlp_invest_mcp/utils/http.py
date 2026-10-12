"""HTTP client helpers for talking to the DLPInvest REST API.

All requests go through :func:`make_request`, which:
- injects the Bearer token from :mod:`dlp_invest_mcp.config`
- normalises success/error envelopes
- logs to **stderr** (stdout is reserved for JSON-RPC)
- respects the ``DLP_INVEST_ACCESS_MODE`` setting to block write operations
- supports GET, POST, PUT, DELETE methods
"""
from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from dlp_invest_mcp.config import settings

logger = logging.getLogger(__name__)


def _build_headers() -> dict[str, str]:
    """Build request headers, including Authorization when a token is set."""
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 dlp-invest-mcp",
    }
    if settings.api_token:
        headers["Authorization"] = settings.api_token
    return headers


def make_request(
    url: str,
    params: dict[str, Any] | None = None,
    method: str = "GET",
) -> dict[str, Any]:
    """Perform a request against the DLPInvest API.
    
    Args:
        url: Path or absolute URL. If relative, joined to ``settings.api_base_url``.
        params: Optional query-string parameters. ``None`` values are filtered out.
        method: HTTP method. Use "GET" for read operations, "POST"/"PUT"/"DELETE" for writes.
            When ``DLP_INVEST_ACCESS_MODE=read``, write methods are blocked.
    
    Returns:
        A dict with ``success`` boolean. On success, contains ``data`` with the
        decoded JSON body. On failure, contains ``error`` and optionally ``message``.
    """
    if not settings.api_token:
        return {
            "success": False,
            "error": "Token de API nao configurado. Defina DLP_INVEST_API_TOKEN.",
        }

    # Check access mode: block write operations when in read-only mode
    if settings.access_mode == "read" and method.upper() not in ("GET",):
        return {
            "success": False,
            "error": "Operacao nao permitida: servidor em modo leitura (DLP_INVEST_ACCESS_MODE=read).",
        }

    full_url = url
    if params:
        filtered = {k: v for k, v in params.items() if v is not None}
        if filtered:
            query = urllib.parse.urlencode(filtered)
            separator = "&" if "?" in full_url else "?"
            full_url = f"{full_url}{separator}{query}"

    if not full_url.startswith("http"):
        full_url = f"{settings.api_base_url}{full_url}"

    req = urllib.request.Request(  # noqa: S310 - URL is controlled/configurable
        full_url,
        headers=_build_headers(),
    )

    try:
        with urllib.request.urlopen(req, timeout=settings.request_timeout_seconds) as resp:
            body = resp.read().decode("utf-8")
            return {"success": True, "data": json.loads(body)}
    except urllib.error.HTTPError as exc:
        message = None
        try:
            message = exc.read().decode("utf-8")
        except Exception:  # pragma: no cover - defensive
            logger.debug("Failed to read HTTP error body", exc_info=True)
        logger.warning("HTTP %s from %s: %s", exc.code, full_url, message or exc.reason)
        result: dict[str, Any] = {"success": False, "error": f"Erro HTTP {exc.code}"}
        if message:
            result["message"] = message
        return result
    except Exception as exc:
        logger.exception("Connection error for %s", full_url)
        return {"success": False, "error": "Erro de coneao", "message": str(exc)}