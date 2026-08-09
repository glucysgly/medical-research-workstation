# Research Workstation Build Plan

## Gate result

Phase -1 is complete. The existing Windows layer is reusable and the WSL2
repair has passed its post-restart gate. Both Windows and Linux-first research
execution can now be selected by the router according to compatibility,
reproducibility and data location.

## Build order

1. **P0 project core** — portable project templates, status transitions,
   project resolver, deterministic researchctl entry point and registry rebuild.
2. **P0 integrity core** — raw-data manifest, hash/provenance records,
   privacy/secret checks, evidence store and result manifest.
3. **P0 research packs** — clinical, qPCR, systematic review/Meta, MR/GWAS and
   public-omics routing contracts; each must point to existing concrete Skills
   and tools in the derived capability view.
4. **P0 verification** — unit/integration/acceptance fixtures and a synthetic
   end-to-end demo using Windows runtimes only.
5. **P1 document and literature adapters** — read-first Zotero health/metadata,
   Obsidian local-file adapter, Quarto/Pandoc/TinyTeX render checks and
   manuscript consistency QC.
6. **P1 WSL integration** — use the repaired bridge for public omics/NGS paths;
   retain before/after health evidence for future baseline changes.
7. **P1 CRI** — housekeeping, retrospectives, feedback, proposals, evals and
   rollback; review-first, protected core excluded.
8. **P2 automations** — report-only dry runs for literature watch, project
   health, reproducibility and review cadence; keep disabled until explicit
   enablement.

## Current completion

- P0 project core: complete; researchctl JSON wrapper and v5 stage history
  verified.
- P0 integrity core: complete; raw manifest, privacy scan, QC, provenance and
  safe reproduce verified.
- P0 research packs: complete; core and optional routing contracts present.
- P0 verification: complete; unit, integration, acceptance, template, CSV/YAML,
  synthetic demo and WSL project smoke checks passed.
- P1 Zotero/Obsidian adapters and P2 report-only automations remain integration
  surfaces; no external write is enabled by default.

## Stop conditions

- Any operation would expose restricted clinical data or secrets.
- A route would require changing the statistical unit, primary outcome, raw
  data or citation integrity.
- A proposed repair would reset/unregister WSL, alter BIOS/security settings,
  install a paid service, upload data or delete existing state without a new
  user decision.
