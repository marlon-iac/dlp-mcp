"""Protocol tests: start the real server and exercise its registered tools."""

from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

from dlp_invest_mcp.config import settings


def _run_server(access_mode: str, methods: list[dict]) -> list[dict]:
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["DLP_INVEST_API_TOKEN"] = ""
    env["DLP_INVEST_ACCESS_MODE"] = access_mode
    # Ensure src/ is on PYTHONPATH so python -m dlp_invest_mcp works
    env["PYTHONPATH"] = str(root / "src") + os.pathsep + env.get("PYTHONPATH", "")

    initialize = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test", "version": "1.0"},
        },
    }
    initialized = {"jsonrpc": "2.0", "method": "notifications/initialized"}
    proc = subprocess.Popen(
        [sys.executable, "-m", "dlp_invest_mcp"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
        env=env,
    )

    def send(msg: dict) -> None:
        assert proc.stdin is not None
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()

    responses: list[dict] = []
    expected_ids = {message["id"] for message in methods if "id" in message}
    stderr_captured = []
    try:
        send(initialize)
        send(initialized)
        for method in methods:
            send(method)

        assert proc.stdout is not None
        for _ in range(len(expected_ids) + 10):
            line = proc.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line:
                responses.append(json.loads(line))
                if responses[-1].get("id") in expected_ids:
                    expected_ids.remove(responses[-1]["id"])
                if not expected_ids:
                    break
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.terminate()
        try:
            _, stderr = proc.communicate(timeout=5)
            stderr_captured.append(stderr)
        except subprocess.TimeoutExpired:
            proc.kill()
            _, stderr = proc.communicate()
            stderr_captured.append(stderr)

    assert not expected_ids, (
        f"Missing response IDs {expected_ids}. Responses: {responses}. Stderr: {stderr_captured}"
    )
    return responses


def _tool_list(access_mode: str) -> tuple[list[str], list[dict]]:
    responses = _run_server(
        access_mode,
        [{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}],
    )
    list_response = next(response for response in responses if response.get("id") == 2)
    assert "result" in list_response, f"Unexpected response: {list_response}"
    tools = list_response["result"]["tools"]
    names = {t["name"] for t in tools}
    return sorted(names), tools


def test_server_lists_tools_according_to_access_mode() -> None:
    """Read mode omits the write tool; write mode advertises it."""
    read_names, _ = _tool_list("read")
    write_names, _ = _tool_list("write")
    expected_read = {
        "obter_operacoes",
        "obter_carteira",
        "obter_posicao",
        "obter_rentabilidade",
        "obter_extrato",
        "obter_proventos",
        "obter_ativos",
        "obter_ativos_detalhes",
        "obter_corretoras",
        "obter_estrategias",
        "obter_subestrategias",
    }
    assert set(read_names) == expected_read
    assert set(write_names) == expected_read | {"adicionar_operacoes"}


def test_registered_tools_dispatch_to_their_implementations() -> None:
    """All registered tools reach their implementation without recursion."""
    names, _ = _tool_list("write")
    responses = _run_server(
        "write",
        [
            {
                "jsonrpc": "2.0",
                "id": index + 2,
                "method": "tools/call",
                "params": {
                    "name": name,
                    "arguments": (
                        {"ticker": "PETR4"}
                        if name == "obter_ativos_detalhes"
                        else {"operacoes": []}
                        if name == "adicionar_operacoes"
                        else {}
                    ),
                },
            }
            for index, name in enumerate(names)
        ],
    )

    calls = [response for response in responses if response.get("id", 0) >= 2]
    assert len(calls) == len(names)
    assert all("Token de API nao configurado" in str(response) for response in calls), calls


def test_server_handlers_delegate_to_tool_implementations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Each registered wrapper forwards its arguments to the matching tool."""
    monkeypatch.setattr(settings, "access_mode", "write")
    handlers = importlib.import_module("dlp_invest_mcp.server")
    handlers = importlib.reload(handlers)

    cases = [
        (
            "obter_operacoes",
            "_obter_operacoes",
            {},
            {
                "carteira": None,
                "status": None,
                "data_inicial": None,
                "data_final": None,
                "limite": 100,
                "offset": 0,
            },
        ),
        ("obter_carteira", "_obter_carteira", {}, {}),
        ("obter_posicao", "_obter_posicao", {"carteira": "principal"}, {"carteira": "principal"}),
        (
            "obter_rentabilidade",
            "_obter_rentabilidade",
            {"data_inicial": "2025-01-01"},
            {"carteira": None, "data_inicial": "2025-01-01", "data_final": None},
        ),
        (
            "obter_extrato",
            "_obter_extrato",
            {"limite": 5},
            {"carteira": None, "data_inicial": None, "data_final": None, "limite": 5, "offset": 0},
        ),
        (
            "obter_proventos",
            "_obter_proventos",
            {},
            {"carteira": None, "data_inicial": None, "data_final": None},
        ),
        ("obter_ativos", "_obter_ativos", {}, {}),
        (
            "obter_ativos_detalhes",
            "_obter_ativos_detalhes",
            {"ticker": "PETR4"},
            {"ticker": "PETR4"},
        ),
        ("obter_corretoras", "_obter_corretoras", {}, {}),
        ("obter_estrategias", "_obter_estrategias", {}, {}),
        ("obter_subestrategias", "_obter_subestrategias", {}, {}),
        (
            "adicionar_operacoes",
            "_adicionar_operacoes",
            {"operacoes": [{"ticker": "PETR4"}]},
            {
                "operacoes": [{"ticker": "PETR4"}],
                "carteira": None,
                "calc": True,
                "return_option": False,
                "validar_duplicadas": False,
            },
        ),
    ]

    try:
        for wrapper_name, implementation_name, arguments, expected_arguments in cases:
            implementation = Mock(return_value={"success": True})
            monkeypatch.setattr(handlers, implementation_name, implementation)

            assert getattr(handlers, wrapper_name)(**arguments) == {"success": True}
            implementation.assert_called_once_with(**expected_arguments)
            implementation.reset_mock()
    finally:
        monkeypatch.undo()
        importlib.reload(handlers)
