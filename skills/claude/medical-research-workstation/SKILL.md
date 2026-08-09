---
name: medical-research-workstation
description: Use for auditable biomedical research workflows including clinical studies, qPCR, systematic reviews, MR/GWAS, public omics, scRNA-seq QC, manuscript checks, reproducibility and submission preparation.
---

# Medical Research Workstation for Claude Code

This is a thin Claude Code adapter. It shares all research, privacy,
statistical-unit, provenance and release rules with `../../shared/` and must
not redefine them.

## Operating contract

1. Read `../../shared/core-manifest.yaml`.
2. Select only the shared reference needed for the current task.
3. Resolve project metadata before reading research outputs.
4. Prefer deterministic local scripts and explicit runtime checks.
5. Preserve human gates for restricted data, high-risk inference and submission.
6. Verify generated artifacts and report limitations.

Never emit credentials, private paths, patient data, private notes or
unverified scientific claims. A successful command is not proof of scientific
validity.

## Platform boundary

Claude-specific behavior is limited to task invocation, working-directory and
permission handling. The canonical research behavior is in `../../shared/`.
External MCP, database and bioinformatics capabilities remain optional and
user-managed.
