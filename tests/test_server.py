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

    responses: list[dict] = []
    stderr_captured = []
    try:
        send(initialize)
        send(initialized)
        send(list_tools)

        assert proc.stdout is not None
        # Read lines. We expect 2 JSON responses (for id=1 and id=2)
        for _ in range(5):
            line = proc.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line:
                responses.append(json.loads(line))
                # Stop if we got the second response
                if responses[-1].get("id") == 2:
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

    list_response = next((r for r in responses if r.get("id") == 2), None)
    assert list_response is not None, (
        f"Could not find response with id=2. Responses: {responses}. Stderr: {stderr_captured}"
    )
    assert "result" in list_response, f"Unexpected response: {list_response}"
    tools = list_response["result"]["tools"]
    names = {t["name"] for t in tools}
    expected = {
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
    missing = expected - names
    assert not missing, f"Missing tools: {missing}"
