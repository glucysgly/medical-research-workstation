# MLRO V2 baseline audit

Date: 2026-08-19

## Existing workstation

- Repository: the local checkout containing this `medical-literature` module
- Branch: `master`
- Existing V5 project/control-plane tests are outside this submodule and were
  not modified.
- The repository had pre-existing user modifications in
  `NATURAL_LANGUAGE_UX_REPORT.json`, `NATURAL_LANGUAGE_UX_REPORT.md`, and
  `scripts/run_nl_ux_acceptance.py`; the V2 change avoided those files.
- No existing MLRO V1 implementation was found. Literature directories were
  README-only, so this is a new isolated V2 submodule rather than an in-place
  V1 migration.

## Runtime observations

| Component | Observation | Status |
|---|---|---|
| Git | 2.55.0.windows.3 | PASS |
| Python | 3.14.7 | PASS |
| uv | 0.12.1 | PASS |
| Node/npm | 24.19.0 / 11.17.0 | PASS |
| SQLite | 3.50.4 | PASS |
| WSL2 | Ubuntu/default distro present; PowerShell output had encoding noise | WARN / not required for Windows core |
| Zotero process | Not running during audit | MANUAL_REQUIRED |
| Codex MCP CLI | Direct PowerShell invocation had console redirection error | MANUAL_REQUIRED |
| Commercial DB credentials | Not inspected or emitted | AUTH_REQUIRED |

## Baseline conclusion

The Windows standard-library core can be added without a second Python/WSL
stack. Vendor MCP registration, external service smoke tests, and commercial
database access remain separate gates.
