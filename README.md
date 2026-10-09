# dlp-invest-mcp

[![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)](https://pypi.org/project/dlp-invest-mcp/)
[![License](https://img.shields.io/pypi/l/dlp-invest-mcp)](https://github.com/marlo-iac/dlp-mcp/blob/main/LICENSE)
[![CI](https://github.com/marlo/dlp-invest-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/marlo/dlp-invest-mcp/actions/workflows/ci.yml)

MCP (Model Context Protocol) server exposing your **DLPInvest** portfolio as tools for AI assistants — Claude Desktop, Cursor, Claude Code, Windsurf, and any MCP-compatible client.

---

## ⚠️ Pré-requisito importante

Antes de configurar o MCP, certifique-se de ter o **`uv`** instalado em sua máquina. O `uv` é a ferramenta moderna e ultrarrápida que gerencia e executa este servidor automaticamente em segundo plano.

- **Windows (PowerShell):**
  ```powershell
  powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **macOS / Linux:**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

---

## Configuração no Cursor (`.cursor/mcp.json`)

Você pode configurar o MCP de duas formas:

### Exemplo 1: Via PyPI (Recomendado para uso normal)
Baixa e executa a última versão publicada no PyPI.

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

### Exemplo 2: Desenvolvimento Local (Usando a wheel gerada)
Útil se você estiver testando modificações locais no código sem precisar publicar no PyPI. Primeiro gere a wheel com `uv build` no seu terminal e aponte para o arquivo `.whl` gerado na pasta `dist/`.

```json
{
  "mcpServers": {
    "dlp-invest-local": {
      "command": "uvx",
      "args": ["--from", "C:/caminho/para/dlp-invest-mcp/dist/dlp_invest_mcp-0.1.6-py3-none-any.whl", "dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui"
      }
    }
  }
}
```

---

## ⚠️ Solução para Erros de Hardlink no Windows (OneDrive / Partições)

Se ao iniciar o MCP você receber o erro `os error 396` (hardlink incompatível), adicione `--link-mode` e `copy` nos argumentos (`args`), evitando problemas em pastas sincronizadas na nuvem:

```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["--link-mode", "copy", "dlp-invest-mcp"],
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
- `obter_operacoes`, `obter_carteira`, `obter_posicao`, `obter_rentabilidade`, `obter_extrato`, `obter_proventos`, `obter_ativos`, `obter_ativos_detalhes`, `obter_corretoras`, `obter_estrategias`, `obter_subestrategias`.

---

## Licença

MIT — see [LICENSE](LICENSE).

