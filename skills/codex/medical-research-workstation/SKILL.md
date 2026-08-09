---
name: medical-research-workstation
description: Use for biomedical research project routing, clinical data or qPCR QC, systematic review and meta-analysis planning, MR/GWAS, public omics, scRNA-seq QC, manuscript QC, reproducibility and submission preparation when an auditable, privacy-aware workflow is needed.
---

# Medical Research Workstation for Codex

Use this adapter to recognize the task, resolve the project and invoke the
smallest relevant shared reference or deterministic runner. It is not a
replacement for domain-specific scientific judgment.

## Operating contract

1. Read `../../shared/core-manifest.yaml`.
2. Read only the matching reference from `../../shared/` and the relevant
   `domain-packs/` contract.
3. Check privacy, biological replicate unit, inputs and human-gate status.
4. Use `scripts/researchctl.py`, a documented project runner or an explicitly
   available external Skill/MCP/CLI.
5. Record provenance and verify outputs before reporting completion.

Never emit credentials, private paths, patient data or full-text private
documents. Never convert a route selection into a claim that analysis ran.

## Trigger examples

`clinical study`, `qPCR`, `systematic review`, `meta-analysis`, `MR`, `GWAS`,
`GEO`, `public omics`, `single-cell`, `scRNA-seq`, `manuscript QC`,
`reproduce`, `provenance`, `submission`.

## Platform boundary

The adapter is platform-specific; research rules remain in `../../shared/`.
Optional Windows, WSL2, R, Python, MCP and database capabilities must be
discovered and verified in the user's environment rather than assumed.
