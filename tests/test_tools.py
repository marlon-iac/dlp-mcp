"""Unit tests for every tool function.

Each test mocks :func:`urllib.request.urlopen` so no network is used.
"""

from __future__ import annotations

import json
import urllib.error
from unittest.mock import patch

import pytest

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
from dlp_invest_mcp.utils import http


class _FakeResponse:
    """Minimal context-manager stand-in for ``urllib.request.urlopen``."""

    def __init__(self, payload: dict) -> None:
        self._payload = json.dumps(payload).encode("utf-8")

    def __enter__(self) -> _FakeResponse:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return self._payload


def _patch_urlopen(payload: dict):
    """Return a patch context that yields a fake HTTP 200 response."""
    return patch("urllib.request.urlopen", return_value=_FakeResponse(payload))


@pytest.fixture()
def _token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure a token is configured so requests are attempted."""
    monkeypatch.setattr(http.settings, "api_token", "DLP-test-token")


@_patch_urlopen({"operations": [], "total": 0})
def test_obter_operacoes(_mock: object, _token: None) -> None:
    result = obter_operacoes(carteira="minha-carteira")
    assert result["success"] is True
    assert result["data"]["total"] == 0


@_patch_urlopen({"id": "minha-carteira", "nome": "Principal"})
def test_obter_carteira(_mock: object, _token: None) -> None:
    result = obter_carteira()
    assert result["success"] is True
    assert result["data"]["id"] == "minha-carteira"


@_patch_urlopen({"posicao": []})
def test_obter_posicao(_mock: object, _token: None) -> None:
    result = obter_posicao(carteira="minha-carteira")
    assert result["success"] is True


@_patch_urlopen({"rentabilidade": 0.05})
def test_obter_rentabilidade(_mock: object, _token: None) -> None:
    result = obter_rentabilidade(data_inicial="2024-01-01", data_final="2024-12-31")
    assert result["success"] is True
    assert result["data"]["rentabilidade"] == 0.05


@_patch_urlopen({"extrato": []})
def test_obter_extrato(_mock: object, _token: None) -> None:
    result = obter_extrato(limite=10, offset=5)
    assert result["success"] is True


@_patch_urlopen({"proventos": []})
def test_obter_proventos(_mock: object, _token: None) -> None:
    result = obter_proventos()
    assert result["success"] is True


@_patch_urlopen({"ativos": ["PETR4", "VALE3"]})
def test_obter_ativos(_mock: object, _token: None) -> None:
    result = obter_ativos()
    assert result["success"] is True
    assert "PETR4" in result["data"]["ativos"]


@_patch_urlopen({"ticker": "PETR4", "nome": "Petrobras"})
def test_obter_ativos_detalhes(_mock: object, _token: None) -> None:
    result = obter_ativos_detalhes("PETR4")
    assert result["success"] is True
    assert result["data"]["ticker"] == "PETR4"


@_patch_urlopen({"corretoras": ["XP", "Clear"]})
def test_obter_corretoras(_mock: object, _token: None) -> None:
    result = obter_corretoras()
    assert result["success"] is True


@_patch_urlopen({"estrategias": ["Buy & Hold"]})
def test_obter_estrategias(_mock: object, _token: None) -> None:
    result = obter_estrategias()
    assert result["success"] is True


@_patch_urlopen({"subestrategias": ["Momentum"]})
def test_obter_subestrategias(_mock: object, _token: None) -> None:
    result = obter_subestrategias()
    assert result["success"] is True


def test_make_request_without_token() -> None:
    """When no token is configured, every tool returns an error envelope."""
    http.settings.api_token = ""
    try:
        result = obter_carteira()
        assert result["success"] is False
        assert "Token" in result["error"]
    finally:
        http.settings.api_token = "DLP-test-token"


def test_make_request_http_error(_token: None) -> None:
    """HTTPError is normalised into the error envelope."""
    err = urllib.error.HTTPError(
        url="https://example.com/carteira",
        code=404,
        msg="Not Found",
        hdrs=None,
        fp=None,
    )
    with patch("urllib.request.urlopen", side_effect=err):
        result = http.make_request("/carteira")
    assert result["success"] is False
    assert "404" in result["error"]


def test_make_request_connection_error(_token: None) -> None:
    """Generic exceptions are normalised into the error envelope."""
    with patch("urllib.request.urlopen", side_effect=ConnectionError("boom")):
        result = http.make_request("/carteira")
    assert result["success"] is False
    assert "boom" in result["message"]


def test_make_request_filters_none_params(_token: None) -> None:
    """None params are filtered before building the query string."""
    captured: dict = {}

    def fake_urlopen(req, timeout=None):  # noqa: ANN001
        captured["url"] = req.full_url
        return _FakeResponse({"ok": True})

    with patch("urllib.request.urlopen", side_effect=fake_urlopen):
        result = http.make_request("/operacoes", {"carteira": None, "status": "aberta"})
    assert result["success"] is True
    assert "status=aberta" in captured["url"]
    assert "carteira" not in captured["url"]
