# Clinical-study template

This project is a reusable clinical research workspace. Real clinical data is
`privacy_level: restricted` by default. Never place identifiers, secrets, or
unverified citations in this tree.

- `data/raw/` is immutable: add a versioned ingest rather than editing in place.
- The statistical unit, estimand, primary outcome, eligibility, and outlier rules
  are protected method decisions; changes require a protocol amendment.
- Every analysis run records inputs, commands, software versions, hashes, run ID,
  outputs, warnings, and evidence links under `provenance/`.
- Results must distinguish observed data, verified literature evidence, and
  hypotheses requiring validation.

Start with `project.yaml`, `status.yaml`, and `protocol/README.md`.
