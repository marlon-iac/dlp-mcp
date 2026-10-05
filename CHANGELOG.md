# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.1.0] - 2026-10-05

### Added

- Initial public release of `dlp-invest-mcp`.
- 11 MCP tools: operations, portfolio, positions, returns, statement,
  dividends, assets, asset details, brokerages, strategies, sub-strategies.
- Stdio server using the official `mcp` SDK (FastMCP).
- Configuration via `pydantic-settings` with env vars:
  `DLP_INVEST_API_TOKEN`, `DLP_INVEST_API_BASE_URL`,
  `DLP_INVEST_REQUEST_TIMEOUT_SECONDS`.
- `uvx dlp-invest-mcp` entry point for zero-Python install.
- `ruff`, `mypy --strict`, `pytest --cov` (70% threshold) configured.
- GitHub Actions workflows: CI (lint + typecheck + test on PR) and
  Trusted Publishing (PyPI on `v*` tags).
- README with install, tools table, env vars, troubleshooting.
- AGENTS.md for LLM-driven development.
- MIT license.
