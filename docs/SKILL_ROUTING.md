# Skill routing

Resolve one primary route from the domain pack. Use supporting skills only when
the primary route requires them and record the reason in provenance.

| Task | Route | Minimum gate |
|---|---|---|
| clinical study | clinical-study + `nature-academic-search` | ethics, unit, estimand |
| qPCR | qpcr-study + `nature-data` | biological replicate, QC, normalization |
| life-science evidence review | life-science-evidence-review + `nature-academic-search` + `nature-citation` | species/topic scope, evidence database, DOI/link verification, conclusion traceability |
| proportional engineering | `avoid-overkill` + `diagnosing-bugs` | observed failure, frozen scope, smallest coherent fix, public behavior validation |
| proportional academic writing | `avoid-overkill` + `nature-citation` | strongest supported claim, evidence boundary, no self-weakening or reviewer prebuttal |
| evidence-bound natural-science manuscript revision | `evidence-bound-natural-science-writing` + `avoid-overkill` + `nature-citation` | proportionality contract, evidence contract, design/unit, effect uncertainty, measurement level, discordant evidence, claim-delta regression |
| editable scientific figure redraw | `recreate-scientific-figure-in-drawio` + `nature-figure` | draw.io callable, graph ready, editable primitives, saved/validated `.drawio`, export QA |
| review/meta | systematic-review-meta + `nature-academic-search` | search, extraction, RoB |
| MR/GWAS | mr-gwas + `research` | dataset release, harmonization, assumptions |
| public omics | public-omics + `nature-data` | accession, metadata, batch/QC |
| exploratory | exploratory-analysis + `research` | branch inventory, confirmation path |
| scRNA/NGS/peaks/variants | matching optional route pack | checksums, reference, QC, unit |
