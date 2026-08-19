# Installation and activation

The core has no runtime dependency beyond Python 3.11+ and SQLite. Run it
directly with `python scripts/medlit.py`; a package entry point is also declared
in `pyproject.toml`.

Vendor components are not installed by this change. To activate one, first
copy its locked source under `third_party/`, run its isolated contract tests,
record license/API/rate-limit evidence, then register only the allowlisted
tools in `.codex/config.toml`. Never put API keys in project files.

Commercial database authentication, CNKI human login, Zotero access, MinerU,
PaperQA2, and external full-text behavior must be verified separately.

See `docs/configuration-guide.zh-CN.md` for the exact PowerShell commands,
local-only Zotero export path, formal database export requirements, and the
evidence needed before calling a review complete.
