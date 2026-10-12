"""Protocol tests: start the real server and exercise its registered tools."""

from __future__ import annotations

import asyncio
import importlib
import json
import os
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest

from dlp_invest_mcp.config import settings


def _run_server(
    access_mode: str,
    methods: list[dict],
    api_base_url: str | None = None,
    api_token: str = "",
) -> list[dict]:
    root = Path(__file__).resolve().parents[1]
    env = dict(os.environ)
    env["DLP_INVEST_API_TOKEN"] = api_token
    env["DLP_INVEST_ACCESS_MODE"] = access_mode
    if api_base_url is not None:
        env["DLP_INVEST_API_BASE_URL"] = api_base_url
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


def test_registered_tools_dispatch_to_their_implementations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """MCP calls reach the corresponding API route using a local HTTP fixture."""
    requests: list[dict] = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            self._respond()

        def do_POST(self) -> None:
            self._respond()

        def _respond(self) -> None:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length)) if length else None
            requests.append(
                {
                    "method": self.command,
                    "path": self.path,
                    "body": body,
                    "authorization": self.headers.get("Authorization"),
                }
            )
            response = json.dumps(
                {"method": self.command, "path": self.path, "body": body}
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

        def log_message(self, format: str, *args: object) -> None:
            pass

    api = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = Thread(target=api.serve_forever, daemon=True)
    thread.start()
    api_base_url = f"http://127.0.0.1:{api.server_port}"

    monkeypatch.setattr(settings, "access_mode", "read")
    monkeypatch.setattr(settings, "api_base_url", api_base_url)
    monkeypatch.setattr(settings, "api_token", "DLP-test-token")
    server_module = importlib.import_module("dlp_invest_mcp.server")
    server_module = importlib.reload(server_module)

    try:

        async def exercise_read_tools() -> list[tuple[str, dict]]:
            registered_tools = await server_module.server.list_tools()
            results = []
            for registered_tool in registered_tools:
                arguments = (
                    {"ticker": "PETR4"} if registered_tool.name == "obter_ativos_detalhes" else {}
                )
                result = await server_module.server.call_tool(registered_tool.name, arguments)
                results.append((registered_tool.name, result.model_dump(by_alias=True)))
            return results

        read_results = asyncio.run(exercise_read_tools())

        monkeypatch.setattr(settings, "access_mode", "write")
        server_module = importlib.reload(server_module)

        async def create_operations() -> tuple[set[str], dict]:
            registered_tools = await server_module.server.list_tools()
            names = {tool.name for tool in registered_tools}
            result = await server_module.server.call_tool(
                "adicionar_operacoes",
                {
                    "operacoes": [{"ticker": "PETR4", "quantidade": 10}],
                    "carteira": "principal",
                    "calc": False,
                    "validar_duplicadas": True,
                },
            )
            return names, result.model_dump(by_alias=True)

        write_names, write_result = asyncio.run(create_operations())
    finally:
        api.shutdown()
        api.server_close()
        thread.join(timeout=5)
        monkeypatch.undo()
        importlib.reload(server_module)

    expected_paths = {
        "obter_operacoes": "/operacoes?limite=100&offset=0",
        "obter_carteira": "/carteira",
        "obter_posicao": "/posicao",
        "obter_rentabilidade": "/rentabilidade",
        "obter_extrato": "/extrato?limite=100&offset=0",
        "obter_proventos": "/proventos",
        "obter_ativos": "/ativos",
        "obter_ativos_detalhes": "/ativos/PETR4",
        "obter_corretoras": "/corretoras",
        "obter_estrategias": "/estrategias",
        "obter_subestrategias": "/subestrategias",
    }
    read_requests = requests[:-1]
    assert len(read_requests) == len(expected_paths)
    assert all(request["method"] == "GET" for request in read_requests)
    assert all(request["authorization"] == "DLP-test-token" for request in read_requests)

    assert len(read_results) == len(expected_paths)
    for tool_name, response in read_results:
        data = response["structuredContent"]["data"]
        assert data["path"] == expected_paths[tool_name], tool_name
        assert data["method"] == "GET", tool_name

    assert "adicionar_operacoes" in write_names
    write_data = write_result["structuredContent"]["data"]
    assert write_data["method"] == "POST"
    assert write_data["path"] == (
        "/operacoes?carteira=principal&calc=False&return_option=False&validar_duplicadas=True"
    )
    assert write_data["body"] == [{"ticker": "PETR4", "quantidade": 10}]
    post_request = requests[-1]
    assert post_request["method"] == "POST"
    assert post_request["authorization"] == "DLP-test-token"
    assert post_request["body"] == [{"ticker": "PETR4", "quantidade": 10}]
