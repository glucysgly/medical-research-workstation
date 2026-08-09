# Architecture

~~~text
Codex Desktop
      │
      ▼
Thin Research Router
      │
      ├── Project Resolver
      ├── Skill Registry
      ├── Risk / Privacy Gate
      ├── Context Budget
      ├── Deterministic Tool Router
      └── QA Router
      │
      ▼
researchctl + Git + R/renv + Python/uv + Quarto + adapters
      │
      ▼
Project text sources of truth
  project.yaml / status.yaml / manifests / plans / evidence / results
      │
      ▼
Reports + provenance + registry index + CRI review
~~~

## Source of truth

Portable text files are authoritative. The registry index is rebuildable and must never be the only copy of project state.

## Context levels

- Level 0: user request, project.yaml, status.yaml, config/skill-index.yaml.
- Level 1: project AGENTS.md, selected Skill, registry records.
- Level 2: specific analysis files, literature notes, data dictionary, logs.
- Level 3: full PDF, full manuscript, notebook or large history only when required.

## Windows / WSL boundary

Windows owns Codex Desktop, Zotero, Obsidian, Office and GUI work. WSL owns Linux-first reproducible analysis and heavy bioinformatics when a working distro and tools are available. Do not duplicate large data or share one environment directory between Windows and WSL.

## Change levels

- E0: maintenance, indexing, documentation, fixtures and registry rebuild.
- E1: low-risk deterministic optimization with tests.
- E2: routing, dependency, MCP, automation or template behavior changes; sandbox + eval + rollback.
- E3: protected research integrity, privacy, raw-data, citation and human decision rules; manual approval only.
