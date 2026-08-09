# Core change policy

Changes to `skills/shared/`, privacy gates, statistical-unit rules,
provenance schemas, release scanners or human-gate behavior are Protected Core
changes.

Every such change requires:

1. a written rationale and scope;
2. a regression test or fixture;
3. an updated core manifest version;
4. a privacy/license audit;
5. review of Codex and Claude adapter consistency;
6. explicit release notes.

Platform-specific adapters must call shared contracts instead of copying them.
Automatic promotion of core changes is disabled.
