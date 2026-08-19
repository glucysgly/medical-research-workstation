# V2 known-item validation

Status: `LIVE_SMOKE_PASS / FORMAL_FREEZE_PENDING`.

`fixtures/search/known_items.yaml` now contains seven mandatory direct-evidence
records and three contextual records for locally advanced cervical cancer with
immunotherapy and definitive chemoradiotherapy. PMID/DOI metadata was checked
against the supplied review reference list and PubMed.

The test engine reports recall and fails a formal strategy when a mandatory
known item is missing. A live recall PASS still requires a database-specific
query, run ID, retrieval date, raw export, and a fresh comparison against the
seven mandatory records. Metadata verification is not a substitute for that
live search test. A current PubMed fallback smoke recovered all 7 mandatory
records (7/7) from 84 returned records using this topic query:

```text
("cervical cancer"[Title/Abstract]) AND
("chemoradiotherapy"[Title/Abstract] OR "chemoradiation"[Title/Abstract]) AND
(pembrolizumab OR durvalumab OR atezolizumab OR nivolumab OR toripalimab)
```

This is a recall smoke test, not a formal review freeze: a formal review still
needs the database-specific export, full provenance manifest, trial registry
search, citation snowball, challenger review, screening, and protocol-defined
eligibility decisions.
