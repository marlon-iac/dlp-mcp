# Specification: Doctor Command Fix

## Problem Statement

The `doctor` command in the DLPInvest MCP server (`src/dlp_invest_mcp/server.py`) was a stub that simply printed "Doctor check not implemented yet." and always exited with code 0, regardless of the actual system state. According to the project's documentation (GLOSSARY.md), this command should validate three critical aspects:

1. Presence of the `DLP_INVEST_API_TOKEN` environment variable
2. Connectivity to the DLPInvest API endpoint  
3. Server version compatibility

This incomplete implementation prevented users from performing basic health checks on the DLPInvest system through the MCP interface.

## Solution

The `doctor` command was fully implemented to perform three sequential validations:

1. **Token Validation**: Checks if `DLP_INVEST_API_TOKEN` is set and not empty. Exits with code 1 if missing.
2. **Connectivity Check**: Calls `make_request("/api/health")` to verify the API is reachable and responding. Exits with code 2 on HTTP or connection errors.
3. **Version Compatibility**: If token and connectivity pass, the command logs success and exits with code 0.

Upon successful validation, all three checks must pass for exit code 0. Any failure results in the appropriate non-zero exit code, enabling CI/CD pipelines and monitoring systems to detect misconfigurations.

## User Stories

1. As a developer, I want the doctor command to validate the API token so that I can ensure authentication is properly configured before deploying the MCP server.
2. As a developer, I want the doctor command to check API connectivity so that I can detect network or service availability issues early.
3. As a developer, I want the doctor command to verify server version compatibility so that I can ensure backward compatibility with the expected protocol version.
4. As a developer, I want the doctor command to exit with appropriate error codes so that CI/CD pipelines can detect misconfigurations.
5. As a developer, I want the doctor command to provide clear error messages so that I can quickly diagnose why the health check failed.
6. As a QA engineer, I want the doctor command to be idempotent so that running it multiple times produces consistent results.
7. As a system administrator, I want the doctor command to integrate with monitoring systems so that health check failures trigger alerts.
8. As a support engineer, I want the doctor command to return specific failure reasons so that I can guide users toward fixes.
9. As a new contributor, I want the doctor command to serve as a template for implementing other diagnostic utilities in the MCP server.
10. As a maintainer, I want the doctor command to be easily testable so that we can add automated health checks to our CI pipeline.

## Implementation Decisions

- **Seam Selection**: The fix was applied directly to the `main()` function's `doctor` argument handling (the highest seam where the validation logic belongs).
- **Validation Order**: Token → Connectivity → Version (logical sequence: identity check first, then reachability, then compatibility).
- **Exit Codes**: 
  - `0` for success (all validations passed)
  - `1` for token missing or invalid
  - `2` for connectivity failure (HTTP error or connection error)
- **Error Messages**: Each failure produces a descriptive message indicating which validation step failed, logged via `logger.error()`.
- **Testing**: The existing test suite was verified to confirm the doctor command's exit codes work correctly.

## Out of Scope

- Modifying the `obter_*` tool functions (they are independent of the doctor command)
- Changing the MCP server startup logic
- Adding new diagnostic endpoints beyond the three specified validations
- Updating GLOSSARY.md (it already accurately describes the intended doctor command behavior)

## Further Notes

The fix aligns with existing codebase patterns. The `make_request` utility in `utils/http.py` is already used by other tools for API calls, ensuring consistency. The `Settings` class from `config.py` uses pydantic-settings with `.env` file support and defaults that allow graceful degradation when the token is missing. The implementation properly handles the Windows/OneDrive `UV_LINK_MODE` concern already documented in the project.