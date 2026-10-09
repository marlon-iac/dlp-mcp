# dlp-invest-mcp

[![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![License](https://img.shields.io/pypi/l/dlp-invest-mcp)](https://github.com/marlo-iac/dlp-mcp/blob/main/LICENSE)
[![CI](https://github.com/marlo-iac/dlp-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/marlo-iac/dlp-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server exposing your **DLPInvest** portfolio as tools for AI assistants — Claude Desktop, Cursor, Claude Code, Windsurf, and any MCP-compatible client.

## What is this?

[MCP](https://modelcontextprotocol.io) is an open protocol that lets AI assistants interact with external tools and data sources. 

This package enables your AI to safely read and query your DLPInvest investment portfolio (positions, trades, statements, dividends, performance) in real-time, **without writing code or running installation scripts**.

---

## Quick Setup (Zero Terminal Commands)

You do **not** need to install Python packages manually. Just add the configuration block below to your AI client's settings.

### Cursor

Add to `.cursor/mcp.json` in your project root or in your global Cursor settings:

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

### Claude Desktop

Paste into your configuration file:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

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

### Claude Code

Run once:

```bash
claude mcp add dlp-invest --scope user --env DLP_INVEST_API_TOKEN=DLP-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx -- uvx dlp-invest-mcp
```

> **Requirement:** Requires [uv](https://docs.astral.sh/uv/) installed on your machine (`uvx` is included automatically with uv).

---

## Available Tools

Once configured, your AI assistant automatically gains access to 11 financial tools:

| Tool | Description | Key Parameters |
| --- | --- | --- |
| `obter_operacoes` | List operations/trades | `carteira`, `status`, `data_inicial`, `data_final`, `limite`, `offset` |
| `obter_carteira` | Retrieve portfolio summary | — |
| `obter_posicao` | Current asset holdings | `carteira` |
| `obter_rentabilidade` | Portfolio returns over a period | `carteira`, `data_inicial`, `data_final` |
| `obter_extrato` | Financial transactions statement | `carteira`, `data_inicial`, `data_final`, `limite`, `offset` |
| `obter_proventos` | Dividends & income received | `carteira`, `data_inicial`, `data_final` |
| `obter_ativos` | List available assets | — |
| `obter_ativos_detalhes` | Asset details by ticker | `ticker` (required, e.g. PETR4) |
| `obter_corretoras` | List registered brokerages | — |
| `obter_estrategias` | List investment strategies | — |
| `obter_subestrategias` | List sub-strategies | — |

---

## Environment Variables

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `DLP_INVEST_API_TOKEN` | *(empty)* | Recommended | Your DLPInvest API token. If omitted, queries return a clear notice asking for the token. |
| `DLP_INVEST_API_BASE_URL` | `https://users.dlpinvest.com.br` | No | Base URL of the DLPInvest REST API. |
| `DLP_INVEST_REQUEST_TIMEOUT_SECONDS` | `30` | No | Timeout in seconds for HTTP requests. |

---

## Troubleshooting

| Problem | Cause | Solution |
| --- | --- | --- |
| `uvx: command not found` | `uv` is not installed | Install `uv` once on your machine ([uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)). |
| "Token de API nao configurado" | `DLP_INVEST_API_TOKEN` missing | Add your token in the `env` section of your MCP configuration JSON. |
| Tools don't appear in AI client | Incorrect configuration JSON | Ensure the JSON is saved inside your client's config file and restart the client. |

---

## License

MIT — see [LICENSE](LICENSE).

