# Reproducibility

Every formal run has a unique run ID and a manifest containing input paths,
SHA-256 hashes, commands, software versions, parameters, outputs, warnings,
evidence references, and reviewer/QA status. Derived files retain their raw
manifest and statistical unit. Results report effect sizes and uncertainty, not
P values alone.

researchctl records the runtime, input/output hashes, command, warnings,
errors and working-tree status for QC runs. reproduce verifies both the raw
manifest and recorded output hashes; it does not silently rerun an unsafe or
unrecorded command.
