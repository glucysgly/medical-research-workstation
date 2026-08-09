# Zotero integration

Use DOI/PMID/title search, then deduplicate before import. Preserve collection,
item key, source metadata, attachment path, and retrieval status in literature
and provenance. Private notes and credentials never enter logs, CSV, JSON, or
external prompts. Verify the final item state after any write.

Local adapter: scripts/zotero_adapter.py. It is read-first and accepts an
explicit Zotero JSON export through --library-json. health, find_item,
get_metadata and export_bib are supported; export_bib writes only when an
explicit local --output is supplied. It never writes to a Zotero library.
