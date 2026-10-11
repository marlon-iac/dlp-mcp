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

**No Windows**, defina a variável de ambiente `UV_LINK_MODE=copy` para evitar erros de hardlink.

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

---

## Tools Disponíveis

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

## 🎯 Exemplos de Perguntas

| Pergunta | Descrição |
|----------|------------|
| "Qual é minha posição atual na DLPInvest?" | Obtém a posição atual do usuário na carteira |
| "Mostre minhas operações recentes" | Lista as operações realizadas na conta |
| "Qual é a rentabilidade da minha carteira?" | Mostra o desempenho financeiro da carteira |
| "Gere um extrato detalhado" | Produz um extrato financeiro completo |
| "Quais corretoras estou usando?" | Lista as corretoras associadas à conta |
| "O que são as minhas estratégias atuais?" | Mostra as estratégias definidas pelo usuário |
| "Detalhe meu ativo mais valioso" | Fornece informações detalhadas sobre o ativo principal |
| "Calcule meu retorno anualizado" | Calcula métricas de retorno financeiro |
| "Mostre os subsistemas ativos" | Lista todos os subsistemas disponíveis |
| "Qual é o valor total da minha carteira?" | Somatório de todos os ativos |

Essas perguntas são apenas exemplos — o MCP suporta até 11 tools diferentes. Cada uma pode ser adaptada conforme as necessidades específicas.

---

## Licença

MIT — veja [LICENSE](LICENSE).