# Skill routing

Resolve one primary route from the domain pack. Use supporting skills only when
the primary route requires them and record the reason in provenance.

| Task | Route | Minimum gate |
|---|---|---|
| clinical study | clinical-study + `nature-academic-search` | ethics, unit, estimand |
| qPCR | qpcr-study + `nature-data` | biological replicate, QC, normalization |
| medical manuscript lifecycle | `medical-manuscript-pipeline` → one phase executor + at most two supporting Skills | mandatory stage gates, evidence/author/submission ledgers, global/local logic, post-freeze author voice, study-type branch, separate document/submission status |
| review/meta | systematic-review-meta + `nature-academic-search` | search, extraction, RoB |
| MR/GWAS | mr-gwas + `research` | dataset release, harmonization, assumptions |
| public omics | public-omics + `nature-data` | accession, metadata, batch/QC |
| exploratory | exploratory-analysis + `research` | branch inventory, confirmation path |
| scRNA/NGS/peaks/variants | matching optional route pack | checksums, reference, QC, unit |
