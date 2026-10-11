# Specification: DLPInvest MCP Server Tool Naming Convention

## Problem Statement

The DLPInvest MCP server contains 11 tool functions exposed to users. According to the `grill-with-docs` skill, tool names should use snake_case without the trailing `_tool` suffix. Some functions were named using the pattern `obter_<resource>_tool` (e.g., `obter_operacoes_tool`), which violates the naming convention and could cause confusion for users interacting with the MCP server.

## Solution
The tool functions have been renamed to follow the `obter_<resource>` pattern (without the `_tool` suffix). This aligns with the established naming convention in the codebase and improves clarity for users.

## User Stories

1. As a developer, I want tool functions to be named consistently with snake_case and without the `_tool` suffix so that the API is easier to understand and maintain.
2. As a user of the DLPInvest MCP server, I want to call tools like `obter_operacoes`, `obter_carteira`, `obter_proventos` so that the API follows standard Python naming conventions.
3. As a QA engineer, I want to ensure all tool functions in the server adhere to the naming convention so that automated checks can validate compliance.
4. As a maintainer, I want to reduce cognitive load when documenting and generating client code because the naming is predictable and consistent.
5. As a new contributor, I want to quickly understand the available tools after reading the server's documentation without having to parse function names.

## Implementation Decisions

- **Modules modified**: `src/dlp_invest_mcp/server.py` - all 11 tool functions were renamed from `obter_*_tool` to `obter_*`.
- **Interface changes**: The function signatures remain unchanged; only the function names were updated. The decorator `@server.tool()` remains the same.
- **Technical clarification**: The change is purely cosmetic (naming convention) and does not affect functionality, serialization, or external compatibility.
- **Schema changes**: None required. The MCP server continues to expose the same methods, just with different names.
- **API contracts**: Unchanged. External clients using the MCP server will need to update their imports if they were relying on the old names.

## Testing Decisions

- **What makes a good test**: A test should verify that the correct function is called with the expected parameters and that the returned dictionary structure is preserved.
- **Which modules will be tested**: The entire `src/dlp_invest_mcp/tools/` directory and the `server.py` file.
- **Prior art**: The codebase already follows the `obter_<resource>` naming pattern internally (e.g., `obter_ativos`, `obter_carteira`, `obter_proventos`), confirming this is the intended convention.

## Out of Scope

- Changing the underlying MCP server implementation or adding new tools beyond the 11 existing ones.
- Modifying the tool implementations themselves (only the names were changed).
- Updating client code that depends on the old function names (this would require separate dependency management).

## Further Notes

- The naming change was driven by the `grill-with-docs` skill requirement to remove the `_tool` suffix from tool names.
- All 11 tools have been updated consistently: `obter_operacoes_tool` → `obter_operacoes`, `obter_carteira_tool` → `obter_carteira`, `obter_posicao_tool` → `obter_posicao`, `obter_rentabilidade_tool` → `obter_rentabilidade`, `obter_extrato_tool` → `obter_extrato`, `obter_proventos_tool` → `obter_proventos`, `obter_ativos_tool` → `obter_ativos`, `obter_ativos_detalhes_tool` → `obter_ativos_detalhes`, `obter_corretoras_tool` → `obter_corretoras`, `obter_estrategias_tool` → `obter_estrategias`, `obter_subestrategias_tool` → `obter_subestrategias`.
- The internal tool imports in `server.py` were already using the correct names (`obter_operacoes`, `obter_carteira`, etc.), so no import changes were needed.
- This change improves consistency with the rest of the codebase, which already uses `obter_<resource>` for the actual tool implementations.
