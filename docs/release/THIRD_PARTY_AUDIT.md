# Third-party and license audit

The public candidate does not vendor the installed local Skill, MCP, CLI,
Zotero, Obsidian, database, paper or runtime collections. It records external
capabilities as references and keeps adapters thin.

| Item | Role | Public decision | License/source evidence |
|---|---|---|---|
| Python standard library | control-plane runtime | KEEP_AS_RUNTIME_DEPENDENCY | Python Software Foundation; no vendored code |
| Git | repository/runtime prerequisite | KEEP_AS_RUNTIME_DEPENDENCY | git-scm.com; no vendored code |
| Codex Skills | optional platform capability | KEEP_AS_EXTERNAL_REFERENCE | installed separately; no third-party bundle copied |
| Claude Code Skills | optional platform capability | KEEP_AS_EXTERNAL_REFERENCE | installed separately; no third-party bundle copied |
| Zotero/MCP | optional read-first integration | KEEP_AS_EXTERNAL_REFERENCE | no library, attachment or credential included |
| GitHub Actions checkout/setup-python | CI actions | KEEP_AS_DEPENDENCY_ONLY | pinned major versions in workflow; upstream licenses remain applicable |
| Local v5.1 reports and pilot data | private evidence | EXCLUDE_FROM_PUBLIC_REPO | intentionally omitted |

Unknown or non-redistributable third-party material is excluded rather than
copied into the repository. Contributors must update the machine-readable
inventory before adding a dependency.
