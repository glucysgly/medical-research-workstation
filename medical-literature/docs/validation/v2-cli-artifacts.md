# V2 CLI artifact validation

Status: `PASS_LOCAL_ARTIFACTS`; provider authorization and human review gates remain explicit.

Validated commands:

| Command | Evidence | Status |
|---|---|---|
| `search-qa --formal-json ... --challenger-json ...` | overlap matrix, challenger unique list, dedup audit | PASS |
| `verify --input ...` | DOI/title/year/provider agreement policy | PASS |
| `freeze --input ... --output SEARCH_FREEZE_MANIFEST.yaml` | UTF-8 manifest, UTC date, SHA-256 | PASS |
| `e2e --output-root ...` | synthetic raw payloads, strategy, overlap, QA, manifest | PASS_OFFLINE_CORE |
| `upstream check` | pinned commits read back without live promotion | LOCKED_UNVERIFIED |
| `audit` | Zotero/MinerU/PaperQA2 local gate report | GATES_REPORTED |

The E2E fixture is synthetic and is not a topic-specific literature result.
The CLI terminal emitter is ASCII-safe so real Chinese titles do not fail on a
GBK PowerShell stdout; persisted JSON/YAML artifacts remain UTF-8.
