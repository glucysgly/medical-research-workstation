# MLRO V2 upstream assessment

Audit date: 2026-08-19. GitHub metadata was read-only. A locked commit is an
audit anchor, not proof of integration readiness.

| Candidate | Locked commit | License signal | Tier/status | Next gate |
|---|---|---|---|---|
| pubmed-search-mcp | `dbcf0c88c76e6fac30877ff16a9850232e89bd4e` | NOASSERTION from API | TIER_B pending license | isolated contract + license review |
| paper-search-mcp | `234678ab231074a7977320978ee0496dcdaddd1f` | MIT | TIER_A candidate | isolated install, tools/list, rate-limit test |
| cnki-skills | `20d65f660456daf53ad0f7c74494ac3b829b925f` | no declared license signal | manual/auth | human login and export test |
| mcp-pubmed-evidence | `f272495c9c3de03791ef45be8b30fc300696c9a7` | MIT | TIER_B fallback candidate | trial search/detail/mapping contract |
| semantic-scholar-skills | `218b02375062954a5ac9f62f85cea12eda3b9d4f` | MIT | TIER_B candidate | isolated install, API terms, live smoke |
| doi-mcp | `000e722c7b93cd0dd1b846570e0138511f8cd89d` | MIT | TIER_B fallback candidate | valid/fake/mismatch golden tests |
| scholar-megasearch | `a24fa3e3274afe84f958279f8b34bc3c67a6b0b5` | MIT | TIER_B challenger | optional install + corpus/provenance test |
| aria-mcp-server | `5624b7c0369c5157c416fd36fa5704c5355c5a8` | MIT | TIER_C optional | do not block core |
| clinical-trials-mcp | `6635fd8e0685e2a16838371d9e9a0f5f8b208123` | ISC | TIER_C experimental | terms/service smoke; disabled by default |
| openalex-mcp-server | `d28b33b32c382cd1d9f563692ab5989f3e801ea6` | Apache-2.0 | TIER_C cross-check | citation-only integration test |

The local implementation uses official fallback boundaries for PubMed,
ClinicalTrials.gov, Semantic Scholar citation edges, and Crossref/PubMed-style
verification. It does not copy vendor internals.

Sources: the repository pages linked in `config/upstreams.lock.yaml`; official
API references are listed in `docs/trial-registry.md` and
`docs/citation-tracing.md`.
