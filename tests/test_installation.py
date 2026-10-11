"""Integration test: verify the package can be built and run via uvx."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def test_build_and_run_uvx() -> None:
    """Run uv build and then uvx to verify installation works."""
    root = Path(__file__).resolve().parents[1]

    # Find uv binary on path
    uv_path = shutil.which("uv")
    if not uv_path:
        pytest.skip("uv binary not found on PATH")

    # 1. Build using uv command
    subprocess.check_call([uv_path, "build", "--wheel"], cwd=str(root))

    # 2. Find the wheel
    dist_dir = root / "dist"
    wheels = list(dist_dir.glob("*.whl"))
    assert len(wheels) >= 1, "No wheel found in dist/"
    wheel_path = max(wheels, key=os.path.getmtime)

    # 3. Run via uvx (uv tool run)
    temp_cache = root / ".uv_test_cache"
    cmd = [
        uv_path,
        "tool",
        "run",
        "--cache-dir",
        str(temp_cache),
        "--link-mode",
        "copy",
        "--from",
        str(wheel_path),
        "dlp-invest-mcp",
    ]

    initialize = '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1"}}}'

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=str(root),
    )

    try:
        stdout, stderr = proc.communicate(input=initialize + "\n", timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        pytest.fail(f"uvx installation test timed out. Stderr: {stderr}")

    assert "Starting DLPInvest MCP server" in stderr
    assert '"result"' in stdout
    assert proc.returncode == 0
