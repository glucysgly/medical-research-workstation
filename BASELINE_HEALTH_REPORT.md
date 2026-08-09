# Baseline Health Report

## Live result

Checked 2026-08-09 on Windows 11 Pro build 26200 before and after restart.

| Layer | Result | Evidence |
|---|---|---|
| Windows control plane | PASS | Existing doctor found Git, Git LFS, GH, Node/npm/pnpm, uv, Python, Quarto, Pandoc, Typst, ImageMagick, rg/fd/jq/fzf, Julia, RStudio, Rscript, TinyTeX and PowerShell 7 |
| Codex proxy setting | PASS | Existing doctor reported system proxy configuration |
| WSL bridge executable | PASS | C:\AI-Workstation\bin\wsl-run.ps1 exists |
| WSL distribution | PASS | HypervisorPresent=true; Ubuntu is available as WSL2 and stopped only when idle |
| WSL bridge regression suite | PASS | 17/17 |
| Linux doctor | PASS | 0 warnings, 0 failures |
| bio-base / R / Bioconductor | PASS | Existing Linux doctor passed the verified baseline tools |
| Research project scaffold | PASS | D-drive project and v5 baseline documents exist |

## Interpretation

The Windows control plane and the repaired WSL2 execution layer are available
for the v5 research delta. The live post-restart result supersedes the earlier
pre-restart failure and the historical report is now consistent with current
health.

## Repair gate

The E2 repair is complete and recorded in WSL_REPAIR_BEFORE.md,
WSL_REPAIR_AFTER.md, and logs/wsl-repair-enable-hypervisor.log. Future WSL
changes still require a before/after health check; no distribution reset or
unregister is authorized by this result.
