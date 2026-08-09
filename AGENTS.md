# Medical Research Workstation Rules

## Authority and versioning

- The active specification is the user-provided v5 prompt:
  Codex_医学科研自动化工作站_最终总控提示词_v5_最优复用版.md.
- v3 is superseded historical material. Do not use it as an execution authority,
  do not copy its design over v5, and do not delete the old source file.
- Phase -1 baseline reconstruction and the derived capability view must be
  completed before adding or replacing infrastructure.

This project is a deterministic research-workstation layer for Codex Desktop. It is not a replacement for scientific judgment.

## Non-negotiable safeguards

- data/raw/ is immutable by default: do not overwrite, delete, or clean in place.
- Real clinical data is privacy_level: restricted unless explicitly classified otherwise.
- Never expose patient identifiers, secrets, tokens, cookies, or private email contents in chat, logs, reports, CSV, JSON, Git, or external services.
- No verified source means no formal citation. Unverified metadata must be marked VERIFY_REQUIRED.
- Never fabricate data, ethics IDs, registration IDs, sample sizes, statistics, citations, or completed analysis.
- Do not delete projects, Zotero collections, Obsidian vaults, raw data, or old Skills automatically.
- Do not push Git, publish repositories, upload restricted data, or enable paid services automatically.
- Do not change primary outcomes, eligibility, statistical units, outlier rules, or protected methods through CRI.

## Routing

1. Resolve the project from project.yaml and status.yaml.
2. Classify the task into RESEARCH, BIO, DATA, DOC, DEV, WEB, DESIGN, SYSTEM, or OPS.
3. Select one primary Skill and at most two supporting Skills unless a written reason is recorded.
4. Prefer deterministic CLI/API/R/Python/SQL steps for structured work; use Codex for design, synthesis, interpretation, and QA.
5. Load the smallest context level needed: project metadata → selected Skill → specific data/results → full documents only when required.
6. Record inputs, commands, hashes, outputs, warnings, and run ID for formal analysis.
7. Verify the artifact before claiming completion.
8. Consult registry/RESEARCH_CAPABILITY_VIEW.csv first, then resolve the
   smallest suitable existing Skill, MCP, plugin, or CLI from the global
   capability index. The project registry is a derived view, not a duplicate
   source of truth.

## Project-specific rules

Project facts belong in project.yaml, current state in status.yaml, data facts in data_dictionary.csv, and scientific evidence in literature/. Do not grow this file with project results.
