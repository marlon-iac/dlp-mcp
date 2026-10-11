# Glossário

## Instalação

Instalar o servidor MCP via `uvx dlp-invest-mcp`. O comando é único e suficiente para uso.

## IDE

Ambiente de desenvolvimento onde o servidor MCP é configurado via arquivo de configuração (`mcp.json` ou equivalente).

## Token

Variável de ambiente `DLP_INVEST_API_TOKEN` usada para autenticação na API DLPInvest. Mantida como variável nos arquivos de configuração do IDE.

## Hardlink

Mecanismo de link de arquivo usado pelo `uvx`. No Windows/OneDrive pode causar `os error 396`. Solução: `--link-mode copy`, oculto do usuário via script de instalação.

## Doctor

Comando `dlp-invest-mcp doctor` que valida presença do token, conectividade e versão do servidor, sem modificar estado.
