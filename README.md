# dlp-invest-mcp

![PyPI](https://img.shields.io/pypi/v/dlp-invest-mcp)
![Python](https://img.shields.io/pypi/pyversions/dlp-invest-mcp)
![License](https://img.shields.io/pypi/l/dlp-invest-mcp)

Servidor MCP que expõe as integrações da **DLPInvest** como tools para assistentes de IA compatíveis com MCP.

---

## ⚠️ Pré-requisito

Antes de configurar o MCP, certifique-se de ter o `uv` instalado.

📖 Veja como instalar: [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/)

---

## ⚡ Como usar

### Configurar o MCP

Copie o exemplo abaixo para o arquivo de configuração do seu IDE e substitua `DLP-seu-token-aqui` pelo seu token. Com o `uv` instalado, a IDE executa `uvx dlp-invest-mcp` ao iniciar o MCP; na primeira execução, o `uvx` baixa e executa o pacote automaticamente.

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

* Read:

  * `obter_operacoes`
  * `obter_carteira`
  * `obter_posicao`
  * `obter_rentabilidade`
  * `obter_extrato`
  * `obter_proventos`
  * `obter_ativos`
  * `obter_ativos_detalhes`
  * `obter_corretoras`
  * `obter_estrategias`
  * `obter_subestrategias`

* Write:
  * `adicionar_operacoes`

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

---

## Licença

MIT — veja [LICENSE](LICENSE).
