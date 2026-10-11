# dlp-invest-mcp

![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)
![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)
![License](https://img.shields.io/pypi/l/dlp-invest-mcp)

Servidor MCP (Model Context Protocol) que expõe a sua carteira da **DLPInvest** como ferramentas para assistentes de IA — Claude Desktop, Cursor, Claude Code, Windsurf e qualquer cliente compatível com MCP.

---

## ⚠️ Pré-requisito

Antes de configurar o MCP, certifique-se de ter o `**uv**` instalado.

📖 Veja como instalar: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

## ⚡ Como usar

### Instalação

```bash
uvx dlp-invest-mcp
```

**No Windows/OneDrive**, defina a variável de ambiente `UV_LINK_MODE=copy` para evitar erros de hardlink (código 396). Isso é suportado nativamente pelo `uv` e não requer scripts auxiliares.

#### Via ambiente:

**PowerShell:**
```powershell
$env:UV_LINK_MODE="copy"
uvx dlp-invest-mcp
```

**Linux/macOS:**
```bash
export UV_LINK_MODE="copy"
uvx dlp-invest-mcp
```

#### Via configuração do cliente (Cursor, Claude, OpenCode)

Adicione `UV_LINK_MODE: "copy"` ao bloco de ambiente do seu cliente:

**Cursor (`~/.cursor/mcp.json` ou `.cursor/mcp.json`):**
```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui",
        "UV_LINK_MODE": "copy"
      }
    }
  }
}
```

**Claude Desktop (`claude_desktop_config.json`):**
```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui",
        "UV_LINK_MODE": "copy"
      }
    }
  }
}
```

**OpenCode:** Adapte conforme o formato do seu configuração de ambiente.

---

### Configurar o MCP

Copie o exemplo abaixo para o arquivo de configuração do seu IDE e substitua `DLP-seu-token-aqui`.

### Cursor (`.cursor/mcp.json`)

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

### Gemini / OpenCode

Adapte o exemplo do Cursor para o arquivo de configuração do seu IDE. O comando permanece `uvx dlp-invest-mcp` e a variável `DLP_INVEST_API_TOKEN` deve estar definida.

---

## Ferramentas Disponíveis

O assistente de IA terá acesso automático a 11 ferramentas financeiras:

- `obter_operacoes`
- `obter_carteira`
- `obter_posicao`
- `obter_rentabilidade`
- `obter_extrato`
- `obter_proventos`
- `obter_ativos`
- `obter_ativos_detalhes`
- `obter_corretoras`
- `obter_estrategias`
- `obter_subestrategias`

---

## Licença

MIT — veja [LICENSE](LICENSE).