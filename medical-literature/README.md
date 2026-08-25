# Medical Literature Research Orchestrator V2 (MLRO V2)

English documentation for the deterministic literature-search and evidence-provenance submodule. For the Chinese guide, see [README.zh-CN.md](README.zh-CN.md).

## Release status

`CORE_READY / OPTIONAL_PENDING`

This package provides a reproducible core for medical literature workflows. It is deliberately honest about provider and authorization boundaries: it does not claim that commercial databases, CNKI, or CENTRAL have been searched when no authorized export or connector is available.

## What is included

- deterministic QUICK, DEEP_DISCOVERY, FORMAL_REVIEW, SEED_EXPANSION, and TRIAL_LANDSCAPE routing;
- source-role separation for formal databases, discovery engines, trial registries, citation tracing, challengers, verifiers, local libraries, and manual imports;
- query linting, canonical normalization, provenance-preserving deduplication, SQLite ledger support, trial normalization, citation edges, verification policy, and search-recall QA;
- official PubMed E-utilities and ClinicalTrials.gov adapters as thin fallbacks;
- bounded Semantic Scholar citation tracing with depth 1 as the default;
- explicit degraded states when optional providers or commercial authentication are unavailable;
- local-only full-text policy, with integration points for Zotero, MinerU, and PaperQA2;
- offline E2E fixtures and standard-library unit/contract/methodology tests.

## Quick start

From this directory:

```powershell
python scripts/medlit.py doctor --json
python scripts/medlit.py capabilities --json
python scripts/medlit.py route "I need a formal systematic review" --json
python scripts/medlit.py strategy --database pubmed --query '(cervical cancer AND immunotherapy)' --json
python scripts/medlit.py e2e --output-root .\runs\offline-e2e
python -m unittest discover -s tests -p 'test_*.py' -v
```

For installation and environment variables, read [docs/configuration-guide.en-US.md](docs/configuration-guide.en-US.md) or [docs/configuration-guide.zh-CN.md](docs/configuration-guide.zh-CN.md).

## Safety and scientific boundaries

- Formal database counts remain separate from discovery and challenger counts.
- Trial registry records remain separate from published papers and are linked by provenance.
- Citation tracing is bounded; unlimited recursive expansion is not enabled by default.
- Commercial database authentication, CNKI CAPTCHA, private Zotero PDFs, and cloud full-text upload require explicit human authorization.
- API keys belong in the local environment or secret store, never in this repository.
- A passing offline test proves the orchestration contract, not the scientific completeness of a live review.

## Public validation boundary

The current public package is `CORE_READY / OPTIONAL_PENDING`. PubMed and ClinicalTrials.gov fallback adapters, citation tracing, normalization, deduplication, provenance, search QA, and offline E2E are represented in code and fixtures. External MCP installation, commercial database access, live challenger comparison, trial-publication mapping at scale, full-text retrieval, risk-of-bias, and evidence synthesis remain explicit downstream gates.

See [docs/validation/v2-final-acceptance.md](docs/validation/v2-final-acceptance.md) for the release acceptance matrix.

## License and upstreams

This submodule contains original integration code and documents the upstream projects it can wrap. Upstream versions and licenses are recorded in [config/upstreams.lock.yaml](config/upstreams.lock.yaml); an upstream lock entry is not a claim that the provider has been installed or accepted into production.
