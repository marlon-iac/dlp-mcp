## Status

Accepted

## Contexto

Usuários leigos precisam instalar o servidor MCP `dlp-invest-mcp` com um comando simples e depois configurar o MCP no IDE. O erro de hardlink `os error 396` no Windows/OneDrive obriga o uso de `--link-mode copy` no `uvx`, mas expor isso ao usuário aumenta a fricção.

## Decisão

- Manter a instalação via `uvx dlp-invest-mcp` como comando único.
- Fornecer scripts de instalação `scripts/install-dlp-invest-mcp.{sh,ps1}` que detectam Windows/OneDrive e executam `uvx` com `--link-mode copy` automaticamente, ocultando a opção do usuário.
- Manter a variável `DLP_INVEST_API_TOKEN` no arquivo de configuração do IDE; sem fluxo interativo de token nesta versão.
- Documentar a configuração do MCP para Gemini, Cursor e OpenCode.
- Adicionar `dlp-invest-mcp --help` com instruções rápidas de instalação e link para docs.
- Adicionar `dlp-invest-mcp doctor` que valida token, conectividade e versão, sem fazer mudanças.

## Consequências

- Reduz fricção inicial e evita erros de hardlink no Windows.
- A escolha de ocultar `--link-mode copy` é irreversível sem quebrar a experiência prometida.
- O não suporte a fluxo interativo de token mantém a superfície de configuração simples e compatível com atuais clientes MCP.
