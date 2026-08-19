# Operations

1. Create a run ID and immutable strategy artifact.
2. Execute each formal database independently and save raw exports.
3. Normalize records and deduplicate while retaining every source.
4. Search ClinicalTrials.gov separately and map publications explicitly.
5. Run citation tracing at depth 1 when in the selected mode.
6. Run challenger QA only for deep/formal modes.
7. Verify identifiers before evidence or manuscript use.
8. Review gaps, then write `SEARCH_FREEZE_MANIFEST.yaml` for a formal review.

If an optional provider fails, record `DEGRADED`/`SKIP` with a warning. Never
retry in a way that violates provider limits, and never overwrite a prior run.
