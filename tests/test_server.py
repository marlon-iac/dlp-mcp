"""Smoke test: start the real server as a subprocess and list tools."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


def test_server_lists_tools() -> None:
    """The server must respond to tools/list with all 11 tools."""
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["DLP_INVEST_API_TOKEN"] = "DLP-test"

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
    list_tools = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}

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

    try:
        send(initialize)
        send(initialized)
        send(list_tools)

        responses: list[dict] = []
        assert proc.stdout is not None
        for _ in range(2):
            line = proc.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line:
                responses.append(json.loads(line))
    finally:
        if proc.stdin:
            proc.stdin.close()
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()

    list_response = next(r for r in responses if r.get("id") == 2)
    assert "result" in list_response, f"Unexpected response: {list_response}"
    tools = list_response["result"]["tools"]
    names = {t["name"] for t in tools}
    expected = {
        "obter_operacoes_tool",
        "obter_carteira_tool",
        "obter_posicao_tool",
        "obter_rentabilidade_tool",
        "obter_extrato_tool",
        "obter_proventos_tool",
        "obter_ativos_tool",
        "obter_ativos_detalhes_tool",
        "obter_corretoras_tool",
        "obter_estrategias_tool",
        "obter_subestrategias_tool",
    }
    missing = expected - names
    assert not missing, f"Missing tools: {missing}"
