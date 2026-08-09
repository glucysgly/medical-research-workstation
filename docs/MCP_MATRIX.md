# MCP and external-service matrix

| Capability | Use | Data boundary | Read-back validation |
|---|---|---|---|
| Zotero | search, metadata, deduplication | no restricted identifiers or private notes | item keys, fields, attachment path |
| Obsidian | local research notes and links | approved vault only; restricted by default | file path and link targets |
| Data widgets | charts/tables from verified derivatives | never upload restricted raw data | source, units, render |
| Web/search | source discovery and verification | send query only; no patient data | URL, date, source status |

External writes, uploads, publication, and paid services require explicit user
authorization and final state read-back.
