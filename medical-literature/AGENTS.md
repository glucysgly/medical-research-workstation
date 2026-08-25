# MLRO V2 local rules

This directory is the literature-search submodule of the Windows-native medical
research workstation. It is a deterministic orchestration layer, not a
replacement for PubMed, ClinicalTrials.gov, Zotero, MinerU, PaperQA2, or human
scientific judgment.

- Keep `FORMAL_DATABASE`, `DISCOVERY_ENGINE`, `TRIAL_REGISTRY`, citation roles,
  `CHALLENGER`, `VERIFIER`, `LOCAL_LIBRARY`, and `MANUAL_IMPORT` distinct.
- Every paper source keeps the query, query hash, run ID, retrieval time,
  identifier, and raw payload path. Never silently merge away provenance.
- Challenger output is QA/discovery only and never changes formal database
  counts. Citation tracing defaults to depth 1.
- Commercial databases, CNKI CAPTCHA, private Zotero PDFs, and cloud full-text
  upload require the appropriate human authorization. Do not bypass access
  control or print secrets.
- The local test suite is standard-library-only and must pass before any live
  provider smoke test. Live results must be stored under a run directory with
  source and timestamp metadata.

## Execution

From this directory:

```powershell
python scripts/medlit.py doctor --json
python scripts/medlit.py capabilities --json
python scripts/medlit.py route "我要做正式系统综述" --json
python -m unittest discover -s tests -p 'test_*.py' -v
```

Do not add API keys to the repository. Use a local environment or user-level
secret store, and only send bibliographic queries, never restricted clinical
data or private full text.
