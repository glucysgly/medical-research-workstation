# Research Workstation Audit

## Scope

This audit records the v5 baseline import and the research-only delta. The
existing Windows/WSL workstation remains the execution substrate; this project
does not replace it or duplicate the global Skill/MCP/CLI registry.

## Baseline

- Active prompt: v5; v3 is historical and superseded.
- Existing workstation: C:\AI-Workstation.
- Global capability source: C:\Users\nmls\Documents\Codex\2026-08-09\zhe\outputs\tooling-capability-index.md.
- Derived research view: registry/RESEARCH_CAPABILITY_VIEW.csv.
- Default privacy: restricted.
- Automation: disabled and report-only by default.

## Live health

- Windows control plane: PASS.
- HypervisorPresent: true.
- WSL2 bridge regression: 17/17 PASS.
- Linux doctor: 0 warnings, 0 failures.
- bio-base and R/Bioconductor baseline: PASS.
- Project visible through WSL bridge: PASS.

Evidence is recorded in BASELINE_HEALTH_REPORT.md, CURRENT_BASELINE.yaml,
WSL_REPAIR_BEFORE.md and WSL_REPAIR_AFTER.md.

## Research layer delivered

- Six reusable core templates and four optional omics/variant templates.
- Core and optional domain routing packs, including compatibility aliases for
  clinical, qPCR and single-cell routes.
- Portable project metadata and v5 stage status history.
- Standard-library researchctl with JSON output.
- Non-destructive raw-data manifest and QC.
- Privacy/secret scan with redacted values and review gates.
- Provenance input/output hashes and safe reproduction verification.
- Derived Skill/MCP/CLI capability catalog and route view.
- Synthetic qPCR-style demo and unit/integration/acceptance tests.

## Remaining controlled work

External Zotero write operations, Obsidian vault restructuring, restricted-data
uploads, Git push, paid services, methodology changes and automatic CRI
promotion remain blocked or require explicit human approval.

The legacy C-drive CodexProjects path was not converted to a junction because
it contains a different pre-existing Auto-Research-Skills tree from the D-drive
tree. A separate migration gate is required before any cutover.
