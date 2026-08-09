# Restore point

Created before workstation implementation: 2026-08-09.

Backup directory:

~~~text
backups/initial-20260809/
~~~

Backed-up items include:

- Codex global AGENTS.md
- Codex config.toml
- Git and WSL configuration when present
- WSL helper script when present
- The capability index used for routing

The backup manifest and SHA-256 values are recorded in the deployment log. Secret values are not printed in reports. Restoring a configuration requires reviewing the target file and making a deliberate copy; no automatic restore is provided.

The backup does not include large research datasets, Zotero libraries, Obsidian vaults, or installed software.

