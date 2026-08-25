# MLRO V2 Public Release Acceptance

## Overall

`CORE_READY / OPTIONAL_PENDING`

This is a generic release assessment. It describes what the repository can
provide without assuming any user's accounts, subscriptions, local files, or
private library.

## Search stack

| Capability | Provider or implementation | Status | Boundary |
|---|---|---|---|
| Formal source roles and provenance | canonical models + ledger | READY_OFFLINE | live database completeness requires fresh runs |
| PubMed | official E-utilities thin adapter | READY_FALLBACK | NCBI email/API key are user-provided |
| Embase | user-authorized native export | AUTH_REQUIRED | no connector assumed |
| Web of Science | user-authorized native export | AUTH_REQUIRED | no connector assumed |
| Scopus | user-authorized native export | AUTH_REQUIRED | no connector assumed |
| CNKI | manual authenticated workflow | MANUAL_REQUIRED | CAPTCHA and login remain human-controlled |
| CENTRAL | manual export workflow | MANUAL_REQUIRED | no brittle crawler |
| Broad discovery | optional paper-search provider | OPTIONAL_UNVERIFIED | does not change formal counts |
| ClinicalTrials.gov | official API v2 thin adapter | READY_FALLBACK | provider limits and live provenance still apply |
| ISRCTN | optional adapter | OPTIONAL_UNVERIFIED | not a core blocker |
| WHO ICTRP | optional adapter | EXPERIMENTAL | may be disabled if upstream is unavailable |
| Citation tracing | bounded Semantic Scholar adapter | READY_FALLBACK | depth 1 default; live API limits apply |
| OpenAlex crosscheck | optional | OPTIONAL_UNVERIFIED | crosscheck only |
| Citation verification | Crossref/PubMed fallback policy | READY_FALLBACK_FIXTURE | live provider agreement must be recorded |
| Search challenger | scholar-megasearch wrapper | OPTIONAL_UNVERIFIED | challenger output is QA/discovery only |
| Zotero | local/Web API integration point | READY_WITH_USER_CONFIG | no secret or private library is shipped |
| MinerU | local tool integration point | READY_WITH_USER_CONFIG | only authorized local/OA PDFs |
| PaperQA2 | local direct-query integration point | READY_WITH_USER_CONFIG | requires a user-supplied LLM provider |

## Methodology and QA

- Formal database counts are separated from discovery, citation, registry, and
  challenger counts.
- The public LACC/PD-1 fixture contains seven mandatory direct-evidence records
  and three contextual records with DOI/PMID metadata checked against a review
  reference list and PubMed.
- A current PubMed fallback smoke recovered 7/7 mandatory LACC/PD-1 records
  from 84 topic-query results; this is a recall smoke, not a formal review
  freeze.
- A formal known-item recall record still requires a database-specific query,
  run ID, retrieval date, raw export, and comparison report.
- Deduplication is DOI-first and preserves provenance; it does not silently
  merge trial registry records with papers.
- Citation tracing defaults to depth 1 and records parent/child edges.
- Offline E2E uses synthetic fixture payloads and does not prove live-review
  completeness.

## Full text and evidence

Local MinerU and PaperQA2 are integration points. The public package does not
ship private PDFs, user API keys, or a claim that all downstream evidence
extraction, risk-of-bias, and synthesis steps are complete. Cloud full-text
upload is disabled by policy unless an explicit user workflow enables a lawful
provider.

## Reproducibility

Every formal run should preserve:

- exact database-specific query;
- search date and run ID;
- hit count and raw export hash;
- source role and provider;
- DOI/PMID normalization and dedup audit;
- trial registry identifiers and publication links;
- citation parent edges and challenger gap review;
- freeze manifest before screening or synthesis.

## Release blockers that remain explicit

The repository is not a claim of a completed formal systematic review. The
following remain user- or provider-dependent: commercial database access,
CNKI/CENTRAL exports, optional MCP installation, live challenger comparison,
large-scale trial-publication mapping, authorized full-text acquisition,
human screening, risk-of-bias assessment, and evidence synthesis.

## Decision

The generic deterministic core is suitable for public release as
`CORE_READY / OPTIONAL_PENDING`. It must not be labelled `FORMAL_REVIEW_READY`
until the missing database-specific searches, raw exports, registry search,
citation snowball, challenger review, screening, and freeze manifest exist for
the actual review question.
