# Recovery

Stop writes first. Preserve the current run ID, logs, manifests, and raw inputs.
Restore only from a verified project snapshot or archive; never use mirror-style
cleanup on `data/raw/`. Compare file count, byte totals, and hashes before
switching paths. Record recovery actions in `retrospective/`.
