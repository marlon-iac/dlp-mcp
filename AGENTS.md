# AGENTS.md - dlp-invest-mcp

Agent-oriented guide. Objective, imperative, verifiable. Keep under 200 lines.

## Overview

`dlp-invest-mcp` is a stdio MCP server exposing 11 DLPInvest portfolio tools.
Stack: Python 3.10+, `mcp` SDK (FastMCP), `pydantic-settings`, stdlib `urllib`.
Target users: AI clients (Claude Desktop, Cursor, Claude Code).

## Directory layout

```
src/dlp_invest_mcp/
├── __init__.py      # version
├── __main__.py      # python -m entry
├── server.py        # FastMCP server + tool decorators
├── config.py        # pydantic-settings (env vars)
├── tools/           # one file per business-logic function
└── utils/
    └── http.py      # make_request() helper
tests/               # pytest suite
```

## Canonical commands

```bash
uv sync                    # install deps + dev tools
uv run ruff check .        # lint
uv run ruff format .       # format
uv run mypy src            # type check (strict)
uv run pytest -q           # tests
uv run dlp-invest-mcp      # run server locally
```

## Conventions

- **New tool**: add function in `src/dlp_invest_mcp/tools/<name>.py`, import into `tools/__init__.py`, wrap with `@mcp.tool()` in `server.py`.
- **Naming**: tools use `obter_<recurso>` (snake_case). Internal wrappers use `<recurso>_tool`.
- **Type hints**: mandatory on all public functions. Use `str | None`, not `Optional[str]`.
- **Docstrings**: Google style on all public functions.
- **Logging**: `logging.getLogger(__name__)` to **stderr only**. Never print to stdout.
- **HTTP**: always go through `make_request()` in `utils/http.py`.

## Adding a new tool (step by step)

1. Create `src/dlp_invest_mcp/tools/meu_tool.py`:

```python
from __future__ import annotations
from typing import Any
from dlp_invest_mcp.utils.http import make_request


def obter_meu_tool(param: str | None = None) -> dict[str, Any]:
    """Description.

    Args:
        param: Explanation.

    Returns:
        Dict with success/data or error.
    """
    return make_request("/meu-endpoint", {"param": param})
```

2. Add to `tools/__init__.py`:

```python
from dlp_invest_mcp.tools.meu_tool import obter_meu_tool
```

3. In `server.py`, register:

```python
from dlp_invest_mcp.tools import obter_meu_tool


@mcp.tool()
def obter_meu_tool_tool(param: str | None = None) -> dict:
    """Description."""
    return obter_meu_tool(param=param)
```

4. Add test in `tests/test_tools.py` with mocked `urlopen`.

5. Run: `uv run pytest -q && uv run ruff check . && uv run mypy src`

## Adding a dependency

Always use `uv add <pkg>` (never edit `pyproject.toml` by hand).

## Pre-commit checklist

- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format .` applied
- [ ] `uv run mypy src` passes
- [ ] `uv run pytest -q` green
- [ ] No secrets committed (use `.env` + `.env.example`)

## Pre-release checklist

- [ ] Bump version in `src/dlp_invest_mcp/__init__.py` and `pyproject.toml`
- [ ] Update `CHANGELOG.md`
- [ ] `git tag vX.Y.Z && git push --tags`
- [ ] CI publishes to PyPI via Trusted Publishing (no token needed)

## Known pitfalls

- **stdout is JSON-RPC** - never `print()` there; use `logging` to stderr.
- **Never commit `DLP_INVEST_API_TOKEN`** - only `.env.example`.
- **Don't import from `tests/`** - tests are not a package consumers use.
- **Don't edit `.github/workflows/`** without reviewing CI impact.
- **Don't add heavy deps** (pandas, numpy) without justification; stdlib `urllib` is enough.

## Where NOT to touch

- `uv.lock` (managed by `uv sync`)
- Generated build artifacts in `dist/`
- `.next/`, `node_modules/` (not part of this project)
