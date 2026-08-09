# v5.1 Core Domain Acceptance

Matrix: `config/domain-acceptance-matrix.json`

| Domain | Overall | Route | Smoke |
|---|---|---|---|
| clinical-observational | PASS | PASS | PASS |
| qpcr | PASS | PASS | PASS |
| systematic-review-meta | PASS | PASS | PASS |
| mr-gwas | WARN | PASS | PASS |
| public-omics-bulk | WARN | PASS | PASS |
| scrna | PASS | PASS | PASS |

## Summary

{"PASS": 4, "WARN": 2, "FAIL": 0, "BLOCKED": 0}

MR/GWAS and public-omics rows deliberately remain input-gated; no synthetic scientific result is promoted.
