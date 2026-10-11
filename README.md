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

1. **Instalar**

```bash
uvx dlp-invest-mcp
```

No Windows/OneDrive, use o script de instalação que aplica `--link-mode copy` automaticamente:

```bash
# PowerShell
./scripts/install-dlp-invest-mcp.ps1
```

1. **Configurar o MCP**

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