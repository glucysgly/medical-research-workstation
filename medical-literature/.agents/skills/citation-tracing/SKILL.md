---
name: citation-tracing
description: Trace backward references and forward citations while preserving edges.
---

# Call when

Call with one to five DOI, PMID, or canonical paper seeds for backward,
forward, related-paper, or snowball discovery.

# Do not call when

Do not recursively expand without an explicit depth decision. Default depth is
1; depth 2 or greater requires explicit opt-in.

# Required outputs

Store `citation_edges` with parent paper, direction, provider, depth, run ID,
and verification status.
