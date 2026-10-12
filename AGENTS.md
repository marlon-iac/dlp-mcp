# AGENTS.md - dlp-invest-mcp

Agent-oriented guide. Objective, imperative, verifiable. Keep under 200 lines.

## Overview

`dlp-invest-mcp` is a stdio MCP server exposing DLPInvest portfolio tools.
Stack: Python 3.10+, `mcp` SDK (MCPServer), `pydantic-settings`, stdlib `urllib`.
Target users: AI clients (Claude Desktop, Cursor, Claude Code, Windsurf e qualquer cliente compatível com MCP).

## Issue tracker

Issues are tracked on GitHub at https://github.com/marlo/dlp-invest-mcp/issues.
See `docs/agents/issue-tracker.md` for triage flow.

## Domain docs

Single-context layout. All domain documentation (`GLOSSARY.md`, `docs/adr/`) lives at the repository root.
See `docs/agents/domain.md` for consumption rules.

## Directory layout

```
src/dlp_invest_mcp/
├ __init__.py      # version
├ __main__.py      # python -m entry
├ server.py        # MCPServer + tool decorators + UV_LINK_MODE fix
├ config.py        # pydantic-settings (env vars)
├ tools/           # one file per business-logic function
└ utils/
    └ http.py      # make_request() helper
tests/               # pytest suite (unit + integration tests)
```

## Canonical commands

```bash
uv sync                    # install deps + dev tools
uv run ruff check .        # lint
uv run ruff format .       # format
uv run mypy src            # type check (strict)
uv run pytest              # unit and integration tests
uv run dlp-invest-mcp      # run server locally
```

## Conventions

- **New tool**: add function in `src/dlp_invest_mcp/tools/<name>.py`, import into `tools/__init__.py`, wrap with `@server.tool()` in `server.py`.
- **Naming**: tools use `obter_<recurso>` (snake_case). Internal wrappers use `<recurso>_tool`.
- **Type hints**: mandatory on all public functions. Use `str | None`, not `Optional[str]`.
- **Docstrings**: Google style on all public functions.
- **Logging**: `logging.getLogger(__name__)` to **stderr only**. Never print to stdout.
- **HTTP**: always go through `make_request()` in `utils/http.py`.

## GOLDEN RULE: No Blind Releases

**NEVER** create a release tag or publish to PyPI without verifying the exact installation artifact locally. The release process is NOT for testing. Tests must pass locally in a simulated production environment first.

## Pre-commit checklist

- [ ] `uv run ruff check .` passes
- [ ] `uv run ruff format .` applied
- [ ] `uv run mypy src` passes
- [ ] `uv run pytest` all green (including `tests/test_installation.py`)
- [ ] No secrets committed (use `.env` + `.env.example`)

## Pre-release checklist (Mandatory)

1. [ ] Bump version in `src/dlp_invest_mcp/__init__.py` and `pyproject.toml`.
2. [ ] Update `CHANGELOG.md`.
3. [ ] **Verify Local Build:**
   ```bash
   uv build
   uvx --from dist/dlp_invest_mcp-<VERSION>-py3-none-any.whl dlp-invest-mcp
   # Manually verify it starts and responds to JSON-RPC if necessary
   ```
4. [ ] `git tag vX.Y.Z && git push --tags`.
5. [ ] Verify GitHub Actions "Publish" job completes successfully.

## Known pitfalls

- **stdout is JSON-RPC** - never `print()` there; use `logging` to stderr.
- **Installation Failures** - `uvx` might fail on Windows/OneDrive due to hardlinks. The code handles this via `os.environ.setdefault("UV_LINK_MODE", "copy")`, but users may still need it in their client config if installation fails before Python runs.
- **Never commit `DLP_INVEST_API_TOKEN`** - only `.env.example`.
- **Don't import from `tests/`** - tests are not a package consumers use.
- **Don't edit `.github/workflows/`** without reviewing CI impact.

## Where NOT to touch

- `uv.lock` (managed by `uv sync`)
- Generated build artifacts in `dist/`
- `.next/`, `node_modules/` (not part of this project)

## Configuration

To control the MCP server behavior, set the following environment variables:

- **`DLP_INVEST_API_TOKEN`**: Authentication token for accessing the DLPInvest API.
- **`DLP_INVEST_ACCESS_MODE`**: Access mode for the server. Use `"read"` for read-only mode (only GET requests are available). Use `"write"` (or leave empty/default) for full access with POST/PUT/DELETE. Set to `"read"` or `"write"` as a string value.

When `DLP_INVEST_ACCESS_MODE=read`, only read operations (GET) are exposed. Write operations (POST, PUT, DELETE) are blocked for security purposes. The default is `"write"` for full access.