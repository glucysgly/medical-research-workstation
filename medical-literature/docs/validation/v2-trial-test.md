# V2 trial adapter validation

Status: `READY_FALLBACK`; live network smoke: `PASS`.

The offline test covers ClinicalTrials.gov API v2 normalization of NCT ID,
title, status, phase, enrollment, conditions, interventions, outcomes, sponsor,
dates, and source. The adapter also implements query pagination and individual
study retrieval through the official API v2 endpoint.

Read-only smoke on 2026-08-19: query `locally advanced cervical cancer`, one
page/one record, returned `NCT06771596` with a non-empty title. The response
was not persisted as a golden scientific set.

The optional mcp-pubmed-evidence, ISRCTN, and WHO ICTRP providers are not
claimed ready.
