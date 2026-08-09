# Public Release Readiness Report

- Project: `medical-research-workstation`
- Internal baseline: `v5.1`
- Public candidate: `v1.0.0-rc1`
- Public candidate branch: `public-release-v1.0.0-rc1`
- Candidate history: fresh sanitized root history; internal workstation history is not included
- Audit date: `2026-08-09`

## Executive result

The public candidate is a portable, reviewable release candidate for an
AI-assisted biomedical research control plane. It contains generic code,
domain contracts, synthetic fixtures and thin platform adapters. It does not
contain the internal workstation reports, real Production Pilot, patient or
restricted data, private notes, Zotero attachments, credentials or large raw
sequencing data.

At this checkpoint, local release checks are complete and the first post-push
GitHub Actions runs for both `main` and the public candidate branch completed
successfully. The candidate packages have been unpacked, privacy-audited and
verified against their SHA-256 manifest.

## Validation matrix

| Check | Expected | Actual | Status | Evidence |
|---|---|---|---|---|
| v5.1 baseline mapping | distinguish internal baseline from public candidate | documented and redacted | PASS | `docs/release/BASELINE_REVIEW.md` |
| public candidate history | no internal history inheritance | fresh root commit | PASS | `git log` on public candidate |
| current-tree privacy/path scan | zero unexplained matches | 232 text files; 0 private-path, secret or PHI/PII matches | PASS | `scripts/public_release_audit.py --strict` |
| unit tests | no failures | 13/13 passed | PASS | `python -m unittest discover -s tests -p "test_*.py" -v` |
| synthetic smoke | deterministic and synthetic-only | route, fixture parsing and safety boundary passed | PASS | `examples/synthetic/run_synthetic_smoke.py` |
| doctor | portable diagnostics | required checks passed | PASS | `scripts/researchctl.py doctor --json` |
| Skill index audit | valid routing index | 13 skills, no audit failures | PASS | `scripts/researchctl.py skills audit --json` |
| bootstrap | bounded, non-installing setup | dry-run and local-directory mode passed | PASS | `scripts/bootstrap.py` |
| Shared Research Core | single source of truth | manifest and shared contracts present | PASS | `skills/shared/` |
| Codex adapter | valid frontmatter and shared references | 35 lines; references shared core | PASS | `skills/codex/medical-research-workstation/SKILL.md` |
| Claude adapter | valid frontmatter and shared references | 30 lines; references shared core | PASS | `skills/claude/medical-research-workstation/SKILL.md` |
| documentation/license | public usage and safety boundaries | README, MIT, security, contribution, disclaimer and release docs present | PASS | repository root and `docs/` |
| GitHub Actions | executable in GitHub | CI passed on `main` and `public-release-v1.0.0-rc1`; current Node 24 action majors are used | PASS | `.github/workflows/`; runs `31312723734`, `31312725160` |
| release package | clean archive and SHA-256 manifest | 3 packages unpacked and audited; all hashes match | PASS | `dist/v1.0.0-rc1-publish/SHA256SUMS.txt` |

## Privacy and security decision

The public tree was scanned without emitting matched text. No current-tree
private user path, credential-shaped value or PHI/PII header was detected.
Internal historical commits were not copied into the public candidate history.
The scanner itself reports counts and redacted paths only.

Raw data, private Zotero/Obsidian content, unpublished manuscripts and external
runtime credentials are excluded. The public default keeps uploads blocked,
Zotero read-first and automation conservative.

## Third-party and license decision

No third-party Skill, MCP, CLI collection, paper, database export or runtime
bundle is vendored. External capabilities are documented as user-managed
references. Python and Git are runtime prerequisites; GitHub Actions are
dependency-only. The public candidate uses MIT for the project code; see
`docs/release/THIRD_PARTY_AUDIT.md` and
`docs/release/third-party-inventory.yaml`.

## Shared Research Core and dual Skills

`skills/shared/core-manifest.yaml` protects raw-data immutability, privacy,
biological replicate rules, provenance/reproduce, evidence and human gates.
The Codex and Claude adapters only route platform behavior and reuse shared
contracts. Changes to this core require a rationale, regression test, manifest
version update, privacy/license review and explicit release notes.

## Platform and research boundary

| Capability | Public status |
|---|---|
| Windows/Python/Git control plane | locally verified |
| WSL2, R, Quarto and external MCP | optional; verify locally |
| Linux/macOS full feature parity | unverified |
| Real clinical or omics analysis | intentionally not included |
| Publication/diagnostic decision support | not claimed |

The synthetic examples validate control flow and safety boundaries only. They
do not validate scientific effect sizes, clinical conclusions, publication
readiness or biological inference.

## Local package artifacts

The publish bundle contains three independently usable artifacts:

- `medical-research-workstation-v1.0.0-rc1.zip`
- `medical-research-workstation-codex-skill-v1.0.0-rc1.zip`
- `medical-research-workstation-claude-skill-v1.0.0-rc1.zip`

`SHA256SUMS.txt` is the authoritative integrity manifest. The full package
and both standalone Skill packages passed post-extraction audit; no matched
private path, secret-shaped value or PHI/PII header was emitted.

## Status summary

- PASS: 14 gates (13 local checks plus post-push CI)
- WARN: 4 limitations (optional runtimes, synthetic-only scope, maintainer
  metadata, release-candidate status)
- FAIL: 0
- BLOCKED: 0 at the local candidate gate
- UNVERIFIED: 0
- DEFERRED: real-data full-cohort analysis, deep Zotero/Obsidian integration,
  cloud deployment, large raw-data download and unverified platform support

## Human decisions and release action

The current task contains the user's explicit authorization to create the
public GitHub repository, push the sanitized candidate and publish a release
candidate. No original workstation branch, tag or data directory is modified.
The repository uses the name `medical-research-workstation`; the citation file
uses a contributor identity rather than inventing a personal institutional
affiliation.

The package artifacts and SHA-256 manifest have been generated and inspected.
The first post-push CI runs passed on both pushed branches. The public-release
audit workflow is additionally configured for manual dispatch and published
release events; a failure there remains a release blocker.
