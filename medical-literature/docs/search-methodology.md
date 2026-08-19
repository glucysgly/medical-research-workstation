# Search methodology

## Modes

`QUICK` uses formal biomedical search plus discovery when configured. It does
not run the full QA chain. `DEEP_DISCOVERY` adds ClinicalTrials.gov, citation
tracing, and the challenger. `FORMAL_REVIEW` requires independent database
queries, trial registries, deduplication, citation snowballing, challenger QA,
gap review, and a freeze manifest. `SEED_EXPANSION` starts from one to five
seeds. `TRIAL_LANDSCAPE` focuses on registered studies. `LIBRARY_ANALYSIS`
starts from a Zotero collection and does not silently broaden the search.

## Strategy artifact

`build_query_artifact` supports PICO, PECO, PCC, SPIDER, PIRD, and PICOTS. The
artifact keeps controlled vocabulary, free terms, drug names, spelling
variants, design filters, date/language limits, and separate database queries.
Formal runs write it to `runs/<run_id>/search_strategy.yaml`.

## Gates

Query lint checks parentheses, phrases, Boolean adjacency, date limits, NOT
use, and duplicate synonyms. Before a formal strategy is locked, 3–10
manually verified known items should be tested; mandatory landmark recall must
be 100%. The current repository includes a five-item placeholder template, not
a fabricated scientific golden set.
