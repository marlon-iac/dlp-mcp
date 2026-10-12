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

**PowerShell:**
```powershell
uvx dlp-invest-mcp
```

**Linux/macOS:**
```bash
uvx dlp-invest-mcp
```

### Configurar o MCP

Copie o exemplo abaixo para o arquivo de configuração do seu IDE e substitua `DLP-seu-token-aqui`.

#### Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui",
        "DLP_INVEST_ACCESS_MODE": "read",
        "UV_LINK_MODE": "copy"
      }
    }
  }
}
```

---

## 🛠️ Tools Disponíveis

O assistente de IA terá acesso às tools financeiras de consulta e, no modo `write`,
à tool de escrita `adicionar_operacoes`:

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
- `adicionar_operacoes`

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
| "Adicione uma nova operação" | adiciona operações via POST /operacoes |

*Essas interações são apenas exemplos*

---

## 🎛️ Modo de Acesso (Read/Write)

- **`DLP_INVEST_ACCESS_MODE=read`** - Modo somente-leitura: tools mutáveis não são expostas e requisições POST/PUT/DELETE são bloqueadas.
- **`DLP_INVEST_ACCESS_MODE=write`** (padrão) - Habilita as tools mutáveis implementadas. Atualmente, `adicionar_operacoes` envia operações para `POST /operacoes`.

Os valores não diferenciam maiúsculas de minúsculas e espaços nas pontas são ignorados. Valores diferentes de `read` e `write` impedem a inicialização do servidor.

### Exemplos de configuração

#### Modo read via ambiente de shell

```bash
# PowerShell
$env:DLP_INVEST_ACCESS_MODE="read"
uvx dlp-invest-mcp

# Linux/macOS
export DLP_INVEST_ACCESS_MODE="read"
uvx dlp-invest-mcp
```

#### Modo write (padrão)

```bash
# Sem a variável ou definida como write
uvx dlp-invest-mcp
# ou
export DLP_INVEST_ACCESS_MODE="write"
uvx dlp-invest-mcp
```

---

## 🛠️ Como desinstalar

Para remover o servidor MCP, basta executar o comando:

```bash
uv tool uninstall dlp-invest-mcp
```

Ou, se instalado via `uvx` diretamente:

```bash
uv tool remove dlp-invest-mcp
```

---

## Licença

MIT — veja [LICENSE](LICENSE).