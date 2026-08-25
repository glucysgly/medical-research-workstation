# MLRO V2 architecture

The V2 layer has one deterministic router and a small set of typed boundaries.

```text
question
  -> mode router
  -> strategy artifact / database-specific queries
  -> formal, discovery, trial, citation, verifier, or challenger adapters
  -> canonical paper/trial models
  -> provenance-preserving deduplication
  -> SQLite ledger + raw payloads
  -> source overlap / recall QA / verification
  -> human gates for screening, full text, evidence, RoB, and synthesis
```

The search roles are intentionally non-interchangeable. A challenger can
identify a query gap but cannot change a formal count. A verifier can flag
metadata conflicts but cannot create a citation. A registry record can map to a
paper but is not itself a publication.

The implementation is standard-library-only and runs on Windows. The official
PubMed E-utilities and ClinicalTrials.gov API v2 adapters are thin fallbacks;
vendor MCPs remain independently locked and require contract/live validation.
