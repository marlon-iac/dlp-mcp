# Glossário

## Instalação

Instalar o servidor MCP via `uvx dlp-invest-mcp`. O comando é único e suficiente para uso.

## IDE

Ambiente de desenvolvimento onde o servidor MCP é configurado via arquivo de configuração (`mcp.json` ou equivalente).

## Token

Variável de ambiente `DLP_INVEST_API_TOKEN` usada para autenticação na API DLPInvest. Mantida como variável nos arquivos de configuração do IDE.

## Hardlink

Mecanismo de link de arquivo usado pelo `uvx`. No Windows/OneDrive pode causar `os error 396`. Solução: `--link-mode copy`, oculto do usuário via script de instalação.

## Acesso

Modo de acesso ao servidor MCP definido pela variável `DLP_INVEST_ACCESS_MODE`:

- **`read`** - Modo somente-leitura: apenas tools de consulta (GET) estão disponíveis.
- **`write`** (padrão) - Acesso completo: todas as tools incluindo POST/PUT/DELETE estão disponíveis.