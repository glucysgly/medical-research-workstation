# V2 MCP tool exposure validation

Status: `NOT_REGISTERED_PENDING_AUTHORIZATION`

The project allowlist exists in `.codex/config.toml`, but no vendor MCP was
installed or registered by this change. The allowlist intentionally exposes
workflow-relevant operations only and excludes duplicate provider tools.

Required next evidence: actual `tools/list` output per server, isolated
contract tests, live smoke tests, version/commit record, and final status
read-back. A configured command alone is not an integration PASS.
