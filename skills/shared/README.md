# Shared Research Core

This directory is the single source of truth for rules shared by the Codex and
Claude Code adapters. Platform adapters may route or format requests, but they
must not duplicate or weaken scientific integrity, privacy, statistical-unit,
provenance or release behavior.

Read progressively:

1. `core-manifest.yaml`
2. the reference that matches the current task
3. the project metadata and runner/schema required by that task

Do not load every domain pack or every external capability by default.
