# v5 Research Workstation Architecture

The workstation is a project-scoped, evidence-aware layer over existing local
skills, CLIs, MCP services, Zotero, and Obsidian. `project.yaml` is project
identity and policy; `status.yaml` is current state; domain packs route methods;
templates provide the file contract; `provenance/` provides run evidence;
`registry/SKILL_CATALOG.csv` is a derived research view of the global index.

Data flow: intake -> classify -> verify access and evidence -> protocol gate ->
immutable raw ingest -> derived data -> analysis -> results -> manuscript and
submission snapshot -> retrospective. Restricted data never leaves approved
paths or enters external services automatically.
