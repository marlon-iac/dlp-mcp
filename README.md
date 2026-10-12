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

#### Cursor (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "dlp-invest": {
      "command": "uvx",
      "args": ["dlp-invest-mcp"],
      "env": {
        "DLP_INVEST_API_TOKEN": "DLP-seu-token-aqui",
        "DLP_INVEST_ACCESS_MODE": "read"
      }
    }
  }
}
```

#### OpenCode / CLI
```bash
# Modo write (padrão, todas as tools disponíveis)
uvx dlp-invest-mcp

# Modo read (apenas consulta)
DLP_INVEST_ACCESS_MODE=read uvx dlp-invest-mcp
```

---

## 🛠️ Tools Disponíveis

O assistente de IA terá acesso automático a 12 tools financeiras:

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
- `adicionar_operacoes` **(nova - POST)**

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
| "Adicione uma nova operação" | **Nova funcionalidade**: adiciona operações via POST /operacoes |

Essas perguntas são apenas exemplos — o MCP suporta 12 tools diferentes. Cada uma pode ser adaptada conforme as necessidades específicas.

---

## 🎛️ Modo de Acesso (Read/Write)

Em vez da antiga variável `DLP_INVEST_READ_ONLY=1`, agora usa-se a variável `DLP_INVEST_ACCESS_MODE` com valores textuais:

- **`DLP_INVEST_ACCESS_MODE=read`** - Modo somente-leitura: apenas tools de GET/read são expostas. Tools de escrita (POST, PUT, DELETE) ficam inacessíveis.
- **`DLP_INVEST_ACCESS_MODE=write`** (padrão) - Acesso completo: todas as tools incluindo POST/PUT/DELETE estão disponíveis.

Isso substitui a antiga `DLP_INVEST_READ_ONLY=1` e oferece uma interface mais intuitiva para o usuário configurar no IDE.

### Como funciona

O servidor respeita a variável `DLP_INVEST_ACCESS_MODE` no momento do início:

- Quando definido como `read`, as tools de escrita (POST, PUT, DELETE) são bloqueadas e não estão disponíveis para o assistente de IA.
- Quando definido como `write` ou não definido (padrão), todas as tools estão disponíveis sem restrições.

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

## 📘 Modo de Leitura-Only

> **Note:** Esta seção foi substituída pela seção "Modo de Acesso (Read/Write)" acima. A variável `DLP_INVEST_READ_ONLY=1` ainda funciona para compatibilidade, mas recomenda-se usar `DLP_INVEST_ACCESS_MODE=read`.

Para configurações de MCP que desejam apenas consultar dados, sem permitir modificações, defina a variável de ambiente:

```bash
DLP_INVEST_READ_ONLY=1
```

Quando ativado, apenas tools de leitura (GET) são expostas. Tools de escrita (POST, PUT, DELETE) ficam inacessíveis. Isso é útil para:

- Configurações de MCP que querem apenas consultar dados
- Ambientes analíticos que não devem modificar dados
- Segurança: impedir escritas acidentais

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