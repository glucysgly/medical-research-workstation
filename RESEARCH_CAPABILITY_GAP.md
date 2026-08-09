# Research Capability Gap Analysis

## Existing capability that will be reused

- Global routing index: tooling-capability-index.md.
- Research Skills: literature search, Nature-style writing/review/data/figures,
  life-science databases, NGS analysis, Zotero import, reproducibility and
  document/PDF/PPT/Excel/LaTeX handling.
- Windows execution: Python, Rscript, Julia, Quarto, Pandoc, Typst, TinyTeX,
  Git/GitHub CLI and deterministic PowerShell.
- Existing WSL bridge: reusable after WSL health is repaired.
- Existing workstation backup and recovery artifacts under C:\AI-Workstation.

## Gaps to build in this project

| Gap | Required v5 layer | Strategy | Priority |
|---|---|---|---|
| Project lifecycle and status | project system | add portable YAML/text metadata and researchctl | P0 |
| Task-to-capability routing | research capability view | derive from global index; do not duplicate it | P0 |
| Data intake and immutable manifest | data QC | deterministic Python/stdlib implementation | P0 |
| Evidence and citation provenance | literature layer | read-first Zotero adapter and evidence files | P0 |
| qPCR safeguards | molecular pack | implement replicate-aware checks and MIQE checklist | P0 |
| Manuscript consistency checks | publication QC | deterministic text/table/figure checks | P1 |
| Provenance and reproduction | reproducibility layer | run records, hashes, environment snapshot | P0 |
| CRI and safe evolution | feedback/optimization | review-first proposal/eval/rollback records | P1 |
| WSL-backed public omics/NGS | execution substrate | repaired and verified; integrate existing NGS Skills with project-level QC | P1 |
| GUI Zotero/Obsidian integration | external adapters | local/read-first, no restructuring or writes by default | P1 |

## Explicit non-gaps

Do not install a second Python/R/Quarto/WSL stack, create a duplicate global
Skill/MCP registry, or replace the existing workstation solely to satisfy a
template.

## Path compatibility note

The canonical new-project root is D:\Users\nmls\Documents\CodexProjects. The
legacy C:\Users\nmls\Documents\CodexProjects path is currently a normal
directory containing a different pre-existing Auto-Research-Skills tree, while
the D-drive tree also contains that project with a different file count and
byte total. Converting C to a junction requires a separately approved
copy/hash/cutover migration; it was not performed during this build.
