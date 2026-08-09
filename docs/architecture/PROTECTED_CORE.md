# Protected Core

The Protected Core is the set of rules that public adapters must not silently
weaken:

- raw data is read-only by default;
- secrets, PHI/PII and private paths are not emitted;
- technical replicates are distinct from biological replicates;
- cells do not automatically become independent donor replicates;
- provenance and reproduction records accompany formal outputs;
- source evidence, uncertainty and limitations remain visible;
- no fabricated data, citations, figures, statistics or completed analyses;
- high-risk analysis and submission remain human-gated;
- public fixtures are synthetic or explicitly redistributable.

The canonical machine-readable record is `skills/shared/core-manifest.yaml`.
Adapters may add platform behavior but must not redefine these rules.
