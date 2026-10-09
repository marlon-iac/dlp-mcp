# dlp-invest-mcp

[![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![License](https://img.shields.io/pypi/l/dlp-invest-mcp)](https://github.com/marlo-iac/dlp-mcp/blob/main/LICENSE)
[![CI](https://github.com/marlo-iac/dlp-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/marlo-iac/dlp-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server exposing your **DLPInvest** portfolio as tools for AI assistants — Claude Desktop, Cursor, Claude Code, Windsurf, and any MCP-compatible client.

---

## ⚠️ Pré-requisito importante

Antes de configurar o MCP, certifique-se de ter o **`uv`** instalado em sua máquina. O `uv` é a ferramenta moderna e ultrarrápida que gerencia e executa este servidor automaticamente em segundo plano.

- **Se você usa Windows (PowerShell):**
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **Se você usa macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
*(Se já tiver o uv instalado, você pode ignorar este passo).*

---

## Configuração Rápida (Sem comandos de terminal)

Basta adicionar o bloco de configuração abaixo no arquivo de configuração da sua IDE ou assistente de IA, substituindo `DLP-seu-token-aqui` pelo seu token da API do DLPInvest.

### Cursor

Adicione em `.cursor/mcp.json` (na raiz do projeto ou nas configurações globais):

```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui"
      }
    }
  }
}
```

### Claude Desktop

Cole no arquivo de configuração do Claude:
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui"
      }
    }
  }
}
```

---

## Ferramentas Disponíveis

O assistente de IA terá acesso automático a 11 ferramentas financeiras:

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

## Variáveis de Ambiente

| Variable | Default | Required | Description |
| --- | --- | --- | --- |
| `DLP_INVEST_API_TOKEN` | *(empty)* | Recommended | Your DLPInvest API token. |
| `DLP_INVEST_API_BASE_URL` | `https://users.dlpinvest.com.br` | No | Base URL of the DLPInvest REST API. |

---

## Licença

MIT — see [LICENSE](LICENSE).
