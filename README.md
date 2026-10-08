# dlp-invest-mcp

[![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![License](https://img.shields.io/pypi/l/dlp-invest-mcp)](https://github.com/marlo/dlp-invest-mcp/blob/main/LICENSE)
[![CI](https://github.com/marlo/dlp-invest-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/marlo/dlp-invest-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server exposing your **DLPInvest** portfolio as tools for AI clients - Claude Desktop, Cursor, Claude Code, and any MCP-compatible client.

## What is this?

[MCP](https://modelcontextprotocol.io) is an open protocol that lets AI models call external tools. This package is a stdio MCP server that talks to the DLPInvest REST API on your behalf. Once configured, an AI assistant can query your positions, trades, dividends, and more - without you writing a single line of code.

**Features:**

- 11 ready-to-use tools covering operations, portfolio, positions, returns, statement, dividends, assets, brokerages, strategies, and sub-strategies.
- Runs over **stdio** (JSON-RPC), the most portable MCP transport.
- Installable via `uvx`, `pip`, or `uv` - no Python knowledge required on the client side.

## Quick install

### Option 1 (recommended): `uvx` + client config

Install [uv](https://github.com/astral-sh/uv) once, then paste the JSON block for your client below.

#### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%AppData%/Claude/claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

#### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

#### Claude Code

```bash
claude mcp add dlp-invest --scope user --env DLP_INVEST_API_TOKEN=DLP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -- uvx dlp-invest-mcp
```

### Option 2: `pip` + manual run

```bash
pip install dlp-invest-mcp
dlp-invest-mcp
```

Then configure your client to run `dlp-invest-mcp` as the command.

## Available tools

| Tool | Description | Key parameters |
| --- | --- | --- |
| `obter_operacoes` | List operations/trades | `carteira`, `status`, `data_inicial`, `data_final`, `limite`, `offset` |
| `obter_carteira` | Portfolio metadata | - |
| `obter_posicao` | Current holdings | `carteira` |
| `obter_rentabilidade` | Returns over a period | `carteira`, `data_inicial`, `data_final` |
| `obter_extrato` | Financial statement | `carteira`, `data_inicial`, `data_final`, `limite`, `offset` |
| `obter_proventos` | Dividends & income | `carteira`, `data_inicial`, `data_final` |
| `obter_ativos` | List all assets | - |
| `obter_ativos_detalhes` | Asset details by ticker | `ticker` (required) |
| `obter_corretoras` | List brokerages | - |
| `obter_estrategias` | List strategies | - |
| `obter_subestrategias` | List sub-strategies | - |

### Example

> What's my current position?

The AI calls `obter_posicao` and returns your holdings in real time.

## Environment variables

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `DLP_INVEST_API_TOKEN` | *(empty)* | No | DLPInvest API token (Bearer). Leave empty to disable requests; tools will return a clear error. |
| `DLP_INVEST_API_BASE_URL` | `https://users.dlpinvest.com.br` | No | Base URL of the DLPInvest REST API. |
| `DLP_INVEST_REQUEST_TIMEOUT_SECONDS` | `30` | No | HTTP request timeout in seconds. |

Settings can also be placed in a `.env` file in the working directory.

## Development

```bash
# Clone
git clone https://github.com/marlo/dlp-invest-mcp
cd dlp-invest-mcp

# Install uv (https://github.com/astral-sh/uv)
# Then:
uv sync                    # install dependencies + dev tools

uv run ruff check .        # lint
uv run ruff format .       # format
uv run mypy src            # type check
uv run pytest -q           # tests
uv run dlp-invest-mcp      # run server locally
```

### Build a local wheel

```bash
uv build
```

Artifacts land in `dist/`. Test install:

```bash
uv pip install dist/dlp_invest_mcp-0.1.0-py3-none-any.whl
```

### Dry-run publish

```bash
uv publish --dry-run
```

## Troubleshooting

| Problem | Likely cause | Fix |
| --- | --- | --- |
| `uvx: command not found` | `uv` not installed | Install uv: `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Tools return "Token de API nao configurado" | `DLP_INVEST_API_TOKEN` missing | Add the env var in your client config or a `.env` file |
| No tools appear in client | Wrong command in client config | Use `uvx dlp-invest-mcp` (not `python ...`) |
| JSON-RPC errors on stdout | Logging writes to stdout | This package logs to stderr only - ensure you did not redirect stderr |
| Timeout / connection errors | Network or wrong base URL | Check `DLP_INVEST_API_BASE_URL` and network access |

## Contributing

1. Fork the repo and create a branch.
2. Run `uv sync` to install dev dependencies.
3. Add tests for any new tool.
4. Ensure `ruff`, `mypy`, and `pytest` pass.
5. Open a PR describing the change.


## License

MIT - see [LICENSE](LICENSE).

